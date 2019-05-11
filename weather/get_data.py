import requests
import pandas as pd
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def get_city_info(city):
    temperature = []
    symbol_var = []
    humidity = []

    appid = 'c0d78490bfcbfdc9dd77405dc48245d0'

    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'q': city, 'units': 'metric', 'APPID': appid})

    data = res.json()
    object_8 = [data['list'][7 + 8 * i] for i in range(5)]
    temperature_list = [obj['main']['temp'] for obj in object_8]
    humidity_list = [obj['main']['humidity'] for obj in object_8]
    symbol_var_list = [obj['weather'][0]['icon'] for obj in object_8]

    temperature.append(temperature_list)
    humidity.append(humidity_list)
    symbol_var.append(symbol_var_list)
    data = pd.DataFrame()
    data['symb'] = symbol_var_list
    symbol_var = data['symb'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                       '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})


    return {'temp' : temperature, 'hum' : humidity, 'symbol' : symbol_var}

