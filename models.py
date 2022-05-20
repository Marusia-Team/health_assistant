from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'

    user_id = Column(String(64), primary_key=True)


class RecipesModel(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ingridients = Column(String(1500), nullable=False)
    cooking_type = Column(String(80), nullable=False)
    recipe = Column(String(8000), nullable=False)
    dish_type = Column(String(80), nullable=False)


class Fitnes1Model(Base):
    __tablename__ = 'fitnes_1'
    exercise_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    body_part = Column(String(50), nullable=False)
    equipment = Column(String(400), nullable=False)
    gif_url = Column(String(1000), nullable=False)
    name = Column(String(1000), nullable=False)
    target = Column(String(500), nullable=False)


class Fitnes2Model(Base):
    __tablename__ = 'fitnes_2'
    exercise_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    body_part = Column(String(50), nullable=False)
    equipment = Column(String(400), nullable=False)
    gif_url = Column(String(1000), nullable=False)
    name = Column(String(1000), nullable=False)
    target = Column(String(500), nullable=False)
