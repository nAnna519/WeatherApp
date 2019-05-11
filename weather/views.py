import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from .weather_model import reg_tree, regressor, icon_dict
from .get_data import get_city_info
import pandas as pd
from requests.exceptions import ConnectionError


# Create your views here.

dictionary = {}
regressor = regressor
reg_tree = reg_tree

def index(request):
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    message = ''
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    cities = City.objects.all()
    cities_name = set([city.name for city in cities])
    cities_information = []

    if (request.method == 'POST'):
        name = request.POST.get('name').lower()
        form = CityForm(request.POST)
        new_city = form.save(commit=False)
        new_city.name = name
        new_city.save()
        if name in cities_name:
            city_to_be_deleted = City.objects.filter(name=name)[0]
            city_to_be_deleted.delete()

    form = CityForm()
    cities = City.objects.all()



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
            information = []
            try:
                for i in range(5):
                    information.append(dictionary[city.name]['temp'][0][i])
                    information.append(dictionary[city.name]['symbol'][i])
                    information.append(dictionary[city.name]['hum'][0][i])
                    # data_frame['temp_' + str(i)] = [temp[i] for temp in dictionary[city.name]['temp']]
                    # data_frame['symbol_var_' + str(i)] = [symbol[i] for symbol in dictionary[city.name]['symbol']]
                    # data_frame['hum_' + str(i)] = [hum[i] for hum in dictionary[city.name]['hum']]
                icon_predict = reg_tree.predict([information])
                new_dict = dict(zip(icon_dict.values(), icon_dict.keys()))

                city_info = {
                    'city': city.name,
                    'temp': round(regressor.predict([information]), 2),
                    # 'icon': response['weather'][0]['icon']
                    'icon' : new_dict[icon_predict.tolist()[0]]
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

    return render(request, 'weather/index.html', context)


def delete(request, name):
    if (request.method == 'POST'):
        city_to_be_deleted = City.objects.filter(name=name.lower())
        city_to_be_deleted.delete()

    cities = City.objects.all()
    cities_information = []

    form = CityForm()
    app_id = 'c0d78490bfcbfdc9dd77405dc48245d0'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    for city in cities:
        try:
            response = requests.get(url.format(city.name)).json()

            city_info = {
                'city': response['name'],
                'temp': response['main']['temp'],
                'icon': response['weather'][0]['icon']
            }
            cities_information.append(city_info)
        except KeyError:
            message = response['message']
            city_to_be_deleted = City.objects.filter(name=city.name)
            city_to_be_deleted.delete()
    cities_information.reverse()
    context = {
        'info': cities_information,
        'form': form
    }

    return redirect('/')

