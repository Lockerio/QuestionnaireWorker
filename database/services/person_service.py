from database.dals.person_dal import PersonDAO


class PersonService:
    def __init__(self, dao: PersonDAO):
        self.dao = dao

    def get_one(self, person_id):
        return self.dao.get_one(person_id)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def delete(self, person_id):
        self.dao.delete(person_id)
