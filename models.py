from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Gender(Base):
    __tablename__ = 'Gender'
    GenderID = Column(Integer, primary_key=True)
    GenderName = Column(String)

class Advancement(Base):
    __tablename__ = 'Advancement'
    AdvancementID = Column(Integer, primary_key=True)
    AdvancementLevel = Column(String)

class User(Base):
    __tablename__ = 'Users'
    UserID = Column(Integer, primary_key=True)
    Nickname = Column(String)
    Age = Column(Integer)
    IDGender = Column(Integer, ForeignKey('Gender.GenderID'))
    IDAdvancement = Column(Integer, ForeignKey('Advancement.AdvancementID'))
    Email = Column(String, unique=True)
    Password = Column(String)

class Exercise(Base):
    __tablename__ = 'Exercise'
    ExerciseID = Column(Integer, primary_key=True)
    ExerciseName = Column(String)

class Stats(Base):
    __tablename__ = 'Stats'
    StatsID = Column(Integer, primary_key=True)
    IDUser = Column(Integer, ForeignKey('Users.UserID'))
    IDExercise = Column(Integer, ForeignKey('Exercise.ExerciseID'))
    RepCount = Column(Integer)
    Weight = Column(Float)
    JumpHeight = Column(Float)