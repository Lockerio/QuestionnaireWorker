from app.database.container import person_service, movement_service
from app.preparers.movement_preparer import MovementPreparer
from app.preparers.person_preparer import PersonPreparer
from app.quesionnaire_parser import QuestionnaireParser


def download_data_and_fill_db(progress_callback):
    questionnaire_parser = QuestionnaireParser()
    person_preparer = PersonPreparer()
    movement_preparer = MovementPreparer()

    # Если есть интернет
    raw_questionnaires_data = questionnaire_parser.get_questionnaires_json()

    # Если интернета нет
    # raw_questionnaires_data = questionnaire_parser.get_questionnaires_json_from_file("../data.json")
    progress_callback.emit("Парсим 'сырые' данные")

    questionnaires_data = raw_questionnaires_data["questionnaires"]
    progress_callback.emit("Данные получены")
    progress_callback.emit("Начинаем заполнение БД")

    total_questionnaires = len(questionnaires_data)
    completed_questionnaires = 0

    for questionnaire in questionnaires_data:
        person_data = person_preparer.get_person_data(questionnaire["name"], questionnaire["socialStatus"])
        person = person_service.create(person_data)
        questionnaire_date = questionnaire["dateMovements"]
        movements = questionnaire["movements"]

        for movement in movements:
            movement_data = movement_preparer.get_movement_data(movement, questionnaire_date, person.id)
            movement_service.create(movement_data)

        # Отображение прогресса
        completed_questionnaires += 1
        if completed_questionnaires % (total_questionnaires // 10) == 0:
            percent_complete = (completed_questionnaires / total_questionnaires) * 100
            print(f"Progress: {percent_complete:.0f}%")

    progress_callback.emit("БД заполнена")
