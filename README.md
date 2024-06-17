WetherApp

This project is a Django application that fetches and stores weather data from the OpenWeatherMap API. 
It allows users to retrieve weather information for random locations within specified latitude and longitude ranges. 
The application uses JWT authentication to protect its API endpoints.
  
## Key Features

- Random Generation of Coordinates: Discover new locations with coordinates ranging from latitude: 8° 4′ to 37° 6′ north and longitude: 68° 7′ to 97° 25′ east.
- Integration with OpenWeatherMap API to fetch weather data.
- Storage of weather data in both a file (`weather_data.txt`) and a database using Django models.
- Authentication using JWT (JSON Web Tokens) to secure API endpoints.
