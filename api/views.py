import json
import random
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from .models import WeatherData
from .serializers import WeatherDataSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.http import Http404
from rest_framework.permissions import AllowAny,IsAuthenticated

class FetchWeatherDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        api_key = settings.OPENWEATHER_API_KEY
        
        # Generate random latitude and longitude
        lat = round(random.uniform(8.0667, 37.1), 6)  # Latitude: 8° 4′ to 37° 6′ north
        lon = round(random.uniform(68.1167, 97.4167), 6)  # Longitude: 68° 7′ to 97° 25′ east
        # lat = -39.667775
        # lon =  11.401196
        print(lat, lon)
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        
        response = requests.get(url)
        data = response.json()

        # Parse relevant data
        location = data.get('name', 'Unknown Location')  # Use 'Unknown Location' if name is missing
        if location == '':
            return Response({"error": "Location not found in API response."}, status=400)

        # Check if the location already exists in the database
        try:
            existing_weather_data = WeatherData.objects.get(location=location)
            serializer = WeatherDataSerializer(existing_weather_data)
            return Response(serializer.data)
        except WeatherData.DoesNotExist:
            pass  # Continue to save the new weather data

        timestamp = timezone.now()
        temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        weather_data = {
            'location': location,
            'timestamp': timestamp.isoformat(),
            'temperature': temperature,
            'humidity': humidity,
            'description': description
        }

        # Write data to file in JSON format
        # if not weather_data['location']:
        #     return Response("could't find a proper location for the request")
        with open('weather_data.txt', 'a') as file:
            file.write(json.dumps(weather_data) + '\n')

        # Save to database
        serializer = WeatherDataSerializer(data=weather_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
    
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        username = serializer.data.get('username')
        password = serializer.data['password']

        # Determine which identifier to use for authentication
        user = None
        if email:
            user = authenticate(request, username=email, password=password)  # Authenticate using email
        elif username:
            user = authenticate(request, username=username, password=password)  # Authenticate using username
        

        if user is not None:
            refresh = RefreshToken.for_user(user)
            print(refresh,"haiii")
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)