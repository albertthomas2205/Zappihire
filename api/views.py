import json
import random
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from .models import WeatherData
from .serializers import WeatherDataSerializer

class FetchWeatherDataView(APIView):

    def get(self, request):
        api_key = settings.OPENWEATHER_API_KEY
        
        # Generate random latitude and longitude
        lat = round(random.uniform(-40, 40), 2)  # Round to 6 decimal places
        lon = round(random.uniform(-40, 40), 2)  # Round to 6 decimal places
        # lat = -39.667775
        # lon =  11.401196
        print(lat,lon)
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        
        response = requests.get(url)
        data = response.json()

        # Parse relevant data
        location = data.get('name', 'Unknown Location')  # Use 'Unknown Location' if name is missing
        if location == 'Unknown Location':
            return Response({"error": "Location not found in API response."}, status=400)

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
      
        if weather_data['location']:
                
            with open('weather_data.txt', 'a') as file:
                file.write(json.dumps(weather_data) + '\n')

        # Save to database
        serializer = WeatherDataSerializer(data=weather_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
