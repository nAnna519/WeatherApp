import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    if (request.method == 'POST'):

        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    cities_information = []

    for city in cities:
        response = requests.get(url.format(city.name)).json()

        city_info = {
            'city': city.name,
            'temp': response['main']['temp'],
            'icon': response['weather'][0]['icon']
        }
        cities_information.append(city_info)

    context = {
        'info': cities_information,
        'form': form
    }

    return render(request, 'weather/index.html', context)