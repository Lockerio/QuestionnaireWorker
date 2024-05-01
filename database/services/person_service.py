from database.dals.person_dal import PersonDAO


class PersonService:
    def __init__(self, dao: PersonDAO):
        self.dao = dao

    def get_one(self, person_id):
        return self.dao.get_one(person_id)

    def get_one_by_full_name(self, full_name):
        return self.dao.get_one_by_full_name(full_name)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        person = self.dao.get_one_by_full_name(data["full_name"])
        if person:
            return self.dao.create(data)
        return person

    def delete(self, person_id):
        self.dao.delete(person_id)
