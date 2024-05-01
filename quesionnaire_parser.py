import json

import requests


class QuestionnaireParser:
    def __init__(self):
        # Ссылка может быть нерабочей, так как СНО "Городская мобильность" собирается
        # переезжать на новый домен. Если ссылка нерабочая, получите новую у Кирилла
        self.url = "https://tl-istu.ru/api/questionnaire?order=ASC"


if __name__ == "__main__":
    _QuestionnaireParser = QuestionnaireParser()
    data = requests.get(_QuestionnaireParser.url).json()
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

