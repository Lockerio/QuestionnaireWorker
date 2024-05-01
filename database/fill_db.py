from icecream import ic

from model.database.container import dadata_token_service, category_service, okved_service, rubric_2gis_service, \
    description_2gis_service
from model.managers.json_manager import JSONManager
from model.secret.tokens import tokens


def get_code_by_label(dictionary, label):
    for code, data in dictionary.items():
        if data["label"] == label:
            return code
    return None


def get_category_title_rubric_label(dictionary, label: str):
    for category_title, data in dictionary.items():
        if label in data["Рубрики"]:
            return category_title
    return "Неизвестно"


if __name__ == "__main__":
    # Заполняем токены
    for token in tokens:
        dadata_token_service.create(token)
    ic()
    # Заполняем категории и ОКВЕДы
    custom_inn_rubrics = JSONManager.read_json("../rubrics/custom_inn_rubrics.json", "utf-8")

    for custom_inn_rubric in custom_inn_rubrics:
        category_service.create({"title": custom_inn_rubric})
        category = category_service.get_one_by_title(custom_inn_rubric)

        for value in custom_inn_rubrics[custom_inn_rubric]:
            okved_service.create({
                "code": str(value),
                "category_id": category.id
            })
    ic()

    # Заполняем дефолтные 2ГИС рубрики и описания
    default_2gis_rubrics = JSONManager.read_json("../rubrics/default_2gis_rubrics.json")
    custom_2gis_rubrics = JSONManager.read_json("../rubrics/custom_2gis_rubrics.json", "utf-8")
    ic()

    for default_2gis_rubric in default_2gis_rubrics.values():
        if default_2gis_rubric["children"]:
            continue

        rubric_data = ic(default_2gis_rubric)
        user_category = category_service.get_one_by_title(
            get_category_title_rubric_label(
                custom_2gis_rubrics,
                rubric_data["label"]
            )
        )

        rubric_2gis_service.create({
            "title": rubric_data["label"],
            "category_id": user_category.id,
            "code": rubric_data["code"]
        })
    ic()

    for custom_2gis_rubric in custom_2gis_rubrics:
        category = category_service.get_one_by_title(custom_2gis_rubric)

        descriptions_2gis = custom_2gis_rubrics[custom_2gis_rubric]["Описание"]
        rubrics_2gis = custom_2gis_rubrics[custom_2gis_rubric]["Рубрики"]

        for description_2gis in descriptions_2gis:
            try:
                description_2gis_service.create({
                    "description": description_2gis,
                    "category_id": category.id
                })
            except Exception:
                continue
    ic()
