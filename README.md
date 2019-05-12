# WeatherApp

This is a simple weather app implemented using python django framework and openweathermap api. It is also complemented by a mathematical model to predict the weather in case ConnectionError.

# Requirements:

  - Python3
  - Django==2.1.4


Library requirements:
  - requests [pip install requests]
  - sklearn [pip install sklearn]
  - pandas [pip install pandas]
  - numpy [pip install numpy]

This application uses openweathermap api for fetching weather details of cities.The official website for api [openweathermap](https://openweathermap.org/).
You have to signup and purchase api key (free api) 


### Installation
follow below steps for application 

```sh
$ cd Django_weather_app
$ python manage.py migrate
$ python manage.py runserver
```

For admin panel access

```sh
$ python manage.py createsuperuser
```

License
by Nikitsinskaya
