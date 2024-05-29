from desktop.utils.graphics_builder import GraphicsBuilder


class QuestionnairesAnalyzer:
    @staticmethod
    def get_people_pie_diagram_figure(df, weekday=None):
        df_copy = df.copy()
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

            count_records = 0

        return GraphicsBuilder.get_pie_diagram_graphic_figure(people_amount_dict, "Распределение типов людей")

    @staticmethod
    def get_types_pie_diagram_figure(df, weekday=None):
        df_copy = df.copy()
        unique_values = df_copy['Место отправления'].unique()
        movement_types_amount_dict = {}

        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        for i_places_type in unique_values:
            count_records = 0
            for j_places_type in unique_values:
                count_records += len(df_copy[(df_copy['Место отправления'] == i_places_type) & (df_copy['Место прибытия'] == j_places_type)])

                if count_records:
                    place_to_place_title = f"{i_places_type} - {j_places_type}"
                    movement_types_amount_dict[place_to_place_title] = count_records

        return GraphicsBuilder.get_pie_diagram_graphic_figure(movement_types_amount_dict, "Распределение типов передвижений")

    @staticmethod
    def get_hours_plot_figure(df, social_status=None, start_point_type=None, weekday=None):
        df_copy = df.copy()

        if social_status:
            df_copy = df_copy[df_copy["Социальный статус"] == social_status]
        if start_point_type:
            df_copy = df_copy[df_copy["Место отправления"] == start_point_type]
        if weekday:
            df_copy = df_copy[df_copy["День недели"] == weekday]

        return GraphicsBuilder.get_plot_graphic_figure(df_copy, social_status, start_point_type)
