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

    def get_person_data(self, raw_person_data):
        person_data = {}
        social_status = self.get_key_by_value(raw_person_data["socialStatus"])

        person_data["full_name"] = raw_person_data["name"]
        person_data["social_status"] = social_status

        return person_data

    def get_key_by_value(self, value):
        for key, values in self.people_types.items():
            if value in values:
                return key
        return None
