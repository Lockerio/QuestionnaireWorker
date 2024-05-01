from typing import Dict, Type, List

from sqlalchemy.orm import Session

from database.models import Person


class PersonDAO:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_one(self, person_id: int) -> Type[Person] | None:
        return self.session.query(Person).get(person_id)

    def get_one_by_full_name(self, full_name: str) -> Type[Person] | None:
        return self.session.query(Person).filter_by(full_name=full_name).first()

    def get_all(self) -> List[Type[Person]] | None:
        return self.session.query(Person).all()

    def create(self, data: Dict):
        person = Person(**data)
        self.session.add(person)
        self.session.commit()
        return person

    def delete(self, person_id: int) -> None:
        person = self.get_one(person_id)
        self.session.delete(person)
        self.session.commit()
