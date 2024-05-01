import collections
import copy

import pandas as pd
from icecream import ic

from model.data_handler import DataHandler
from model.managers.csv_manager import CSVManager


# Читаем файл с данными
df = CSVManager.read_csv(r"C:\Users\Lokerio\Desktop\TL-ISTU выгрузка данных - Лист5.csv")

# Если не нужна фильтрация по городу, то поставьте '#' в начале следующей строки
df = df[df['Город'] == 'Усть-Кут']


# Словарь типов корреспонденций
people_types = collections.OrderedDict({
    "Трудящиеся": ["работающий"],
    "Студенты": ["студент"],
    "Прочие": [
        'временно нетрудящийся (декретный отпуск, отпуск по уходу за ребенком)',
        'пенсионер по возрасту',
        'домохозяйка',
        'человек ограниченными возможностями',
        'школьник',
        'безработный'
    ]
})


# Создаем словарь для поддатафреймов, на все типы людей
sub_dataframes = {}
for people_type_key, people_type_value in people_types.items():
    temp_df = df[df['Социальный статус'].isin(people_type_value)]
    sub_dataframes[people_type_key] = temp_df
sub_dataframes["Все"] = df

every_type = ic(set(DataHandler.get_unique_fields_in_column(df, "Место отправления")))

# Словарь типов точек перемещений
places_types = collections.OrderedDict({
    "Дом": [
        'дом - место жительства'
    ],
    "Работа": [
        'работа - служебная поездка',
        'работа / рабочее место'
    ],
    "Учеба": [
        'университет / институт',
        'школа',
        'колледж / техникум / училище'
    ]
})

# Вычисляем тип 'Прочее'
defined_places = set(item for sublist in places_types.values() for item in sublist)
other_places = every_type - defined_places
places_types["Прочее"] = list(other_places)

# Создаем заголовки для матрицы
output_matrix = collections.OrderedDict({
    "Заголовки": ["Дом", "Работа", "Учеба", "Прочее"]
})

people_types__output_matrix = {sub_dataframe_key: copy.deepcopy(output_matrix) for sub_dataframe_key in sub_dataframes.keys()}

# Считаем матрицы
for people_type_key, sub_dataframe in sub_dataframes.items():
    unique_people = DataHandler.get_unique_fields_in_column(sub_dataframe, "ID").tolist()
    unique_people_amount = len(unique_people)

    ic(people_type_key, unique_people_amount, len(sub_dataframe))

    for places_type_i_key, places_type_i_value in places_types.items():
        for places_type_j_key, places_type_j_value in places_types.items():
            sum_percent = 0
            for places_type_i in places_type_i_value:
                for places_type_j in places_type_j_value:
                    filtered_df = sub_dataframe[(sub_dataframe['Место отправления'] == places_type_i) & (
                                sub_dataframe['Место прибытия'] == places_type_j)]


                    try:
                        percent = len(filtered_df) / unique_people_amount
                    except ZeroDivisionError:
                        percent = 0

                    # ic(percent)
                    sum_percent += percent


            sum_percent = str(sum_percent).replace(".", ",")

            output_matrix = people_types__output_matrix[people_type_key]

            if places_type_i_key in output_matrix.keys():
                output_matrix[places_type_i_key].append(sum_percent)
            else:
                output_matrix[places_type_i_key] = [sum_percent]

ic(people_types__output_matrix)

# Сохраняем матрицы
for title, matrix in people_types__output_matrix.items():
    df = pd.DataFrame(matrix)
    CSVManager.save_csv(df, rf"C:\Users\Lokerio\Desktop\Матрицы\General_matrix__Усть-Кут_{title}.csv", ";")


