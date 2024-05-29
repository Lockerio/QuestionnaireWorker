from matplotlib.figure import Figure


class GraphicsGetter:
    @staticmethod
    def get_plot_graphic_figure(df, people_type, place_type):
        hours = df['Время отправления']

        figure = Figure(figsize=(10, 6))
        ax = figure.add_subplot(111)
        ax.plot(hours.value_counts().sort_index(), marker='o', color='skyblue', linestyle='-')
        ax.set_xlabel('Час')
        ax.set_ylabel('Количество отправлений')
        ax.set_title(f"{people_type}: Отправление '{place_type}'")
        ax.set_xticks(range(24))
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        return figure

    @staticmethod
    def get_pie_diagram_graphic_figure(amount_dict, title):
        labels = list(amount_dict.keys())
        sizes = list(amount_dict.values())

        def my_autopct(pct):
            total = sum(sizes)
            val = int(round(pct * total / 100.0))
            return '{v:d}'.format(p=pct, v=val)

        figure = Figure(figsize=(8, 8))
        ax = figure.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct=my_autopct, startangle=140)
        ax.axis('equal')
        ax.set_title(title)

        return figure
