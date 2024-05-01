from sqlalchemy.orm import Session
from database.db import engine

from database.dals.movement_dal import MovementDAO
from database.dals.person_dal import PersonDAO

from database.services.movement_service import MovementService
from database.services.person_service import PersonService


session = Session(bind=engine)

movement_dao = MovementDAO(session)
person_dao = PersonDAO(session)

movement_service = MovementService(movement_dao)
person_service = PersonService(person_dao)