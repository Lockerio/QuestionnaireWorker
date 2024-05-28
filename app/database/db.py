import os
import sqlalchemy as db
from sqlalchemy.orm import declarative_base


db_path = os.path.join('../..', 'Questionnaires.db')
engine = db.create_engine(f'sqlite:///{db_path}')

Base = declarative_base()
