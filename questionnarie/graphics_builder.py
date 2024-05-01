from matplotlib import pyplot as plt


class GraphicsBuilder:
    @staticmethod
    def create_plot_graphic(df, people_type, place_type):
        hours = df['Время отправления']

        plt.figure(figsize=(10, 6))
        plt.plot(hours.value_counts().sort_index(), marker='o', color='skyblue', linestyle='-')
        plt.xlabel('Час')
        plt.ylabel('Количество отправлений')
        plt.title(f"{people_type}: Отправление '{place_type}'")
        plt.xticks(range(24))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    @staticmethod
    def create_pie_diagram_graphic(amount_dict, title):
        labels = list(amount_dict.keys())
        sizes = list(amount_dict.values())

        def my_autopct(pct):
            total = sum(sizes)
            val = int(round(pct * total / 100.0))
            return '{v:d}'.format(p=pct, v=val)

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct=my_autopct, startangle=140)
        plt.axis('equal')
        plt.title(title)
        plt.show()
