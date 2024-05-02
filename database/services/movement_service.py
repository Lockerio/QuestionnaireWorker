from database.dals.movement_dal import MovementDAO


class MovementService:
    def __init__(self, dao: MovementDAO):
        self.dao = dao

    def get_one(self, movement_id):
        return self.dao.get_one(movement_id)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def delete(self, movement_id):
        self.dao.delete(movement_id)
