import pandas as pd
import geopandas as gpd

from graphics_builder import GraphicsBuilder
from scripts.db_to_df import get_df_from_db


class QuestionnairesAnalyzer:
    def __init__(self, shape_filepath):
        self.df = get_df_from_db()
        self.shape = gpd.read_file(shape_filepath)

    def build_people_pie_diagram(self, weekday=None):
        df_copy = self.df.copy()
        unique_values = df_copy['Социальный статус'].unique()
        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        people_amount_dict = {}

        count_records = 0
        for people_type in unique_values:
            count_records += len(df_copy[df_copy['Социальный статус'] == people_type])

            if count_records:
                title = people_type
                people_amount_dict[title] = count_records

        GraphicsBuilder.create_pie_diagram_graphic(people_amount_dict, "Распределение типов людей")

    def build_types_pie_diagram(self, weekday=None):
        df_copy = self.df.copy()
        unique_values = df_copy['Место отправления'].unique()
        movement_types_amount_dict = {}

        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        for i_places_type in unique_values:
            count_records = 0
            for j_places_type in unique_values:
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
    shape_filepath = r"C:\Users\Lokerio\Desktop\границы_агломерация.shp"
    questionnaire_analyzer = QuestionnairesAnalyzer(shape_filepath)

    # График распределения по времени
    questionnaire_analyzer.build_hours_plot("Трудящиеся", "Дом", "Понедельник".lower())

    # Диаграмма распределения социального статуса
    questionnaire_analyzer.build_people_pie_diagram()

    # Диаграмма распределения типов передвижения
    questionnaire_analyzer.build_types_pie_diagram()
