from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from database.db import Base, engine


class Person(Base):
    __tablename__ = 'Persons'
    id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    full_name = Column(String(), unique=True, nullable=False)
    social_status = Column(String(), nullable=False)


class Movement(Base):
    __tablename__ = 'Movements'
    id = Column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    movement_date = Column(String(), nullable=False)
    week_day = Column(String(), nullable=False)
    departure_place_type = Column(String(), nullable=False)
    arrival_place_type = Column(String(), nullable=False)
    departure_time = Column(String(), nullable=False)
    arrival_time = Column(String(), nullable=False)
    departure_lat = Column(Float(), nullable=False)
    departure_lon = Column(Float(), nullable=False)
    arrival_lat = Column(Float(), nullable=False)
    arrival_lon = Column(Float(), nullable=False)


    person_id = Column(Integer(), ForeignKey('Persons.id'), nullable=False)
    person = relationship("Person")


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)
