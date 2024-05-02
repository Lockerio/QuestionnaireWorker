from tqdm import tqdm

from database.container import person_service, movement_service
from preparers.movement_preparer import MovementPreparer
from preparers.person_preparer import PersonPreparer
from quesionnaire_parser import QuestionnaireParser


questionnaire_parser = QuestionnaireParser()
person_preparer = PersonPreparer()
movement_preparer = MovementPreparer()

raw_questionnaires_data = questionnaire_parser.get_questionnaires_json()
questionnaires_data = raw_questionnaires_data["questionnaires"]

for questionnaire in tqdm(questionnaires_data, total=len(questionnaires_data), desc="Заполнение БД"):
    person_data = person_preparer.get_person_data(questionnaire["name"], questionnaire["socialStatus"])
    person = person_service.create(person_data)
    questionnaire_date = questionnaire["dateMovements"]
    movements = questionnaire["movements"]

    for movement in movements:
        movement_data = movement_preparer.get_movement_data(movement, questionnaire_date, person.id)
        movement_service.create(movement_data)
