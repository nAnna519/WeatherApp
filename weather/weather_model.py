import requests
import json
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os


icon_dict = {'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                         '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02n': 10}

def function():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'city_list.json')
    try:
        with open(filename, encoding='utf-8') as f:
            d = json.load(f)
    except FileNotFoundError as e:
        print(e)

    s_city = [i['name'] for i in d]
    i = 0
    for city in d:
        if city['name'] == '' or city['country'] == '':
            del s_city[i]
        i += 1

    temperature = []
    symbol_var = []
    humidity = []

    temperature_goal = []
    symbol_var_goal = []

    data_frame = pd.DataFrame()

    appid = 'c0d78490bfcbfdc9dd77405dc48245d0'

    for i in range(500):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'q': s_city[i], 'units': 'metric', 'APPID': appid})

            data = res.json()
            object_8 = [data['list'][7 + 8 * i] for i in range(5)]
            temperature_list = [obj['main']['temp'] for obj in object_8]
            humidity_list = [obj['main']['humidity'] for obj in object_8]
            symbol_var_list = [obj['weather'][0]['icon'] for obj in object_8]

            temperature.append(temperature_list)
            humidity.append(humidity_list)
            symbol_var.append(symbol_var_list)

            goal_object = data['list'][0]
            temperature_goal.append(goal_object['main']['temp'])
            symbol_var_goal.append(goal_object['weather'][0]['icon'])
        except Exception as e:
            pass

    for i in range(len(temperature_goal)):
        for i in range(5):
            data_frame['temp_' + str(i)] = [temp[i] for temp in temperature]
            data_frame['symbol_var_' + str(i)] = [symbol[i] for symbol in symbol_var]
            data_frame['hum_' + str(i)] = [hum[i] for hum in humidity]

    data_frame['temp_goal'] = temperature_goal
    data_frame['symbol_goal'] = symbol_var_goal


    def label_encode(le, data, feature, feature_dict):
        try:
            data[feature + '_le'] = data[feature].map(feature_dict[feature]).fillna(-1)
            data = data.drop([feature], axis=1)
        except KeyError:
            le.fit(data[feature].astype(str))
            data[feature + '_le'] = le.transform((data[feature].values))
            feature_dict = dict(zip(le.classes_, le.transform(le.classes_)))
            data = data.drop([feature], axis=1)
            return feature_dict


    def preprocessing_data(data):
        data['symbol_var_0'] = data['symbol_var_0'].map(icon_dict)

        data['symbol_var_1'] = data['symbol_var_1'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                         '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})
        data['symbol_var_2'] = data['symbol_var_2'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                         '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})
        data['symbol_var_3'] = data['symbol_var_3'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                         '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})

        data['symbol_var_4'] = data['symbol_var_4'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                         '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})
        data['symbol_goal'] = data['symbol_goal'].map({'01d': 0, '04d': 1, '03d': 2, '10d': 3, '02d': 4, '10n': 5,
                                                       '04n': 6, '01n': 7, '03n': 8, '13d': 9, '02': 11})
        data = data.dropna()
        return data


    data_frame = preprocessing_data(data_frame)

    X = data_frame.drop(['temp_goal', 'symbol_goal'], axis=1)
    y_temp = data_frame['temp_goal']
    y_symb = data_frame['symbol_goal']

    X_train, X_test, y_temp_train, y_temp_test, y_symb_train, y_symb_test = train_test_split(X, y_temp, y_symb, test_size=0.3, random_state=42)

    regressor = LinearRegression()

    regressor.fit(X_train, y_temp_train)

    # # make a prediction set using the test set
    # prediction = regressor.predict(X_test)

    reg_tree = RandomForestClassifier(max_depth=9, max_features=3, n_estimators=200, random_state=42)

    reg_tree.fit(X_train, y_symb_train)

    return regressor, reg_tree

regressor, reg_tree = function()