from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base, engine


class Person(Base):
    __tablename__ = 'Questionnaires'
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
    departure_points = Column(String(), nullable=False)
    arrival_points = Column(String(), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)