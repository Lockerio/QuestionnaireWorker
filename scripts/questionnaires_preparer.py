import collections

import pandas as pd
from icecream import ic

from model.data_handler import DataHandler
from model.questionnarie.graphics_builder import GraphicsBuilder


class QuestionnairePreparer:
    def __init__(self, df_filepath, shape_filepath):
        self.df = CSVManager.read_csv(df_filepath)
        self.shape = SHXManager.read_shx(shape_filepath)

        self.people_types = collections.OrderedDict({
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

        self.places_types = collections.OrderedDict({
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

        self.every_type = set(DataHandler.get_unique_fields_in_column(self.df, "Место отправления"))

        defined_places = set(item for sublist in self.places_types.values() for item in sublist)
        other_places = self.every_type - defined_places
        self.places_types["Прочее"] = list(other_places)

        self.prepare_df()

    def time_to_hours(self, time_str):
        if ":" in time_str:
            hours, minutes = time_str.split(':')
            if minutes == "00":
                return int(hours)
            if hours == "23":
                return 0
            return int(hours) + 1
        else:
            return 14

    def prepare_df(self):
        self.df['lat'] = 0.0
        self.df['lon'] = 0.0

        for index, row in self.df.iterrows():
            try:
                lat_lon = row['Координаты отправления'].split(', ')
                self.df.at[index, 'lat'] = float(lat_lon[0])
                self.df.at[index, 'lon'] = float(lat_lon[1])
            except:
                pass

        self.df = DataHandler.get_data_by_shape(self.df, self.shape, "lat", "lon")
        self.df['Время отправления'] = self.df['Время отправления'].apply(lambda x: self.time_to_hours(x))
        self.df['День недели'] = pd.to_datetime(self.df['Дата передвижения']).dt.day_name()

        reverse_people_types = {value: key for key, values in self.people_types.items() for value in values}
        reverse_places_types = {value: key for key, values in self.places_types.items() for value in values}

        self.df['Социальный статус'] = self.df['Социальный статус'].map(reverse_people_types)
        self.df['Место отправления'] = self.df['Место отправления'].map(reverse_places_types)
        self.df['Место прибытия'] = self.df['Место прибытия'].map(reverse_places_types)

    def build_people_pie_diagram(self, weekday=None):
        df_copy = self.df.copy()
        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        people_amount_dict = {}

        count_records = 0
        for people_type in self.people_types.keys():
            count_records += len(df_copy[df_copy['Социальный статус'] == people_type])

            if count_records:
                title = people_type
                people_amount_dict[title] = count_records

        GraphicsBuilder.create_pie_diagram_graphic(people_amount_dict, "Распределение типов людей")

    def build_types_pie_diagram(self, weekday=None):
        df_copy = self.df.copy()
        movement_types_amount_dict = {}

        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        for i_places_type in self.places_types.keys():
            count_records = 0
            for j_places_type in self.places_types.keys():
                count_records += len(df_copy[(df_copy['Место отправления'] == i_places_type) & (df_copy['Место прибытия'] == j_places_type)])

                if count_records:
                    place_to_place_title = f"{i_places_type[0].title()} - {j_places_type[0].title()}"
                    movement_types_amount_dict[place_to_place_title] = count_records

        GraphicsBuilder.create_pie_diagram_graphic(movement_types_amount_dict, "Распределение типов передвижений")

    def build_hours_plot(self, social_status=None, start_point_type=None, weekday=None):
        df_copy = self.df.copy()

        if social_status:
            df_copy = df_copy[df_copy["Социальный статус"] == social_status]
        if start_point_type:
            df_copy = df_copy[df_copy["Место отправления"] == start_point_type]
        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        GraphicsBuilder.create_plot_graphic(df_copy, social_status, start_point_type)


if __name__ == "__main__":
    questionnaires_filepath = r"C:\Users\Lokerio\Desktop\TL-ISTU выгрузка данных - Лист5.csv"
    shape_filepath = r"C:\Users\Lokerio\Desktop\границы_агломерация.shp"
    questionnaire_preparer = QuestionnairePreparer(questionnaires_filepath, shape_filepath)

    # График распределения по времени
    questionnaire_preparer.build_hours_plot("Трудящиеся", "Дом", "Monday")

    # Диаграмма распределения социального статуса
    questionnaire_preparer.build_people_pie_diagram()

    # Диаграмма распределения типов передвижения
    questionnaire_preparer.build_types_pie_diagram()
