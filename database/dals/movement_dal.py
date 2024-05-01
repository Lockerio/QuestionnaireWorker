from typing import Dict, Type, List

from sqlalchemy.orm import Session

from database.models import Movement


class MovementDAO:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_one(self, movement_id: int) -> Type[Movement] | None:
        return self.session.query(Movement).get(movement_id)

    def get_one_by_title(self, title: str) -> Type[Movement] | None:
        return self.session.query(Movement).filter_by(title=title).first()

    def get_all(self) -> List[Type[Movement]] | None:
        return self.session.query(Movement).all()

    def create(self, data: Dict):
        movement = Movement(**data)
        self.session.add(movement)
        self.session.commit()
        return movement

    def delete(self, movement_id: int) -> None:
        movement = self.get_one(movement_id)
        self.session.delete(movement)
        self.session.commit()
