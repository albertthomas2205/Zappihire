from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100,unique=True)
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)

        
        

    def __str__(self):
        return f"{self.location} at {self.timestamp}"
    
# d4893334920e3c942eb367cfc13bbd17

# https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API key}  