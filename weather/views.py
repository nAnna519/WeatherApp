import requests
from django.shortcuts import render

# Create your views here.


def index(request):
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id
    city = 'London'

    response = requests.get(url.format(city)).json()

    city_info = {
        'city': city,
        'temp': response['main']['temp'],
        'icon': response['weather'][0]['icon']
    }

    context = {
        'info': city_info
    }

    return render(request, 'weather/index.html', context)