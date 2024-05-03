import json
import requests


class QuestionnaireParser:
    def __init__(self):
        # Ссылка может быть нерабочей, так как СНО "Городская мобильность" собирается
        # переезжать на новый домен. Если ссылка нерабочая, получите новую у Кирилла
        self.url = "https://tl-istu.ru/api/questionnaire?order=ASC"

    def get_questionnaires_json(self):
        questionnaires_json = requests.get(self.url).json()
        return questionnaires_json

    def save_questionnaires_json(self, output_filepath):
        questionnaires_data = self.get_questionnaires_json()
        with open(output_filepath, "w", encoding="utf-8") as json_file:
            json.dump(questionnaires_data, json_file, ensure_ascii=False, indent=4)

    def get_questionnaires_json_from_file(self, filepath):
        with open(filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)

        return data

if __name__ == "__main__":
    questionnaire_parser = QuestionnaireParser()
    questionnaire_parser.save_questionnaires_json("data.json")
