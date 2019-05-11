import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from .weather_model import reg_tree, regressor, icon_dict
from .get_data import get_city_info
from requests.exceptions import ConnectionError


dictionary = {}

def index(request):
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    cities = City.objects.all()
    cities_name = set([city.name for city in cities])

    if (request.method == 'POST'):
        name = request.POST.get('name').lower().title()
        form = CityForm(request.POST)
        new_city = form.save(commit=False)
        new_city.name = name
        new_city.save()
        if name in cities_name:
            city_to_be_deleted = City.objects.filter(name=name)[0]
            city_to_be_deleted.delete()

    form = CityForm()
    cities = City.objects.all()

    context = get_cities_information(url, cities, form)

    return render(request, 'weather/index.html', context)


def delete(request, name):
    if (request.method == 'POST'):
        city_to_be_deleted = City.objects.filter(name=name)
        city_to_be_deleted.delete()

    cities = City.objects.all()

    form = CityForm()
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    get_cities_information(url, cities, form)

    return redirect('/')


def get_cities_information(url, cities, form):

    cities_information = []
    message = ''

    for city in cities:
        try:
            response = requests.get(url.format(city.name)).json()

            city_info = {
                'city': response['name'],
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon']
            }
            cities_information.append(city_info)

            dictionary[city.name] = get_city_info(city.name)
        except ConnectionError:
            message = 'No internet connection.'
            information = []
            try:
                for i in range(5):
                    information.append(dictionary[city.name]['temp'][0][i])
                    information.append(dictionary[city.name]['symbol'][i])
                    information.append(dictionary[city.name]['hum'][0][i])
                icon_predict = reg_tree.predict([information])
                new_dict = dict(zip(icon_dict.values(), icon_dict.keys()))

                city_info = {
                    'city': city.name,
                    'temp': round(regressor.predict([information]).tolist()[0], 2),
                    'icon': new_dict[icon_predict.tolist()[0]]
                }
                cities_information.append(city_info)
            except KeyError:
                message = 'No internet connection.'
                city_to_be_deleted = City.objects.filter(name=city.name)
                city_to_be_deleted.delete()
        except KeyError:
            message = response['message']
            city_to_be_deleted = City.objects.filter(name=city.name)
            city_to_be_deleted.delete()
    cities_information.reverse()
    context = {
        'info': cities_information,
        'form': form,
        'message': message
    }
    return context
