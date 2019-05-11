import requests
import pandas as pd
from .weather_model import icon_dict


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
    symbol_var = data['symb'].map(icon_dict)


    return {'temp' : temperature, 'hum' : humidity, 'symbol' : symbol_var}

