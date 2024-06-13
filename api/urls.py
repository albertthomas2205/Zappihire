from django.urls import path
from .views import FetchWeatherDataView

urlpatterns = [
    path('fetch_weather/', FetchWeatherDataView.as_view(), name='fetch-weather-data'),
]