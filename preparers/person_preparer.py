class PersonPreparer:
    def __init__(self):
        self.people_types = {
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
        }

    def get_person_data(self, name, social_status):
        person_data = {"full_name": name, "social_status": social_status}
        return person_data

    def get_key_by_value(self, value):
        for key, values in self.people_types.items():
            if value in values:
                return key
        return None
