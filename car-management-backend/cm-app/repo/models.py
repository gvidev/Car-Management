from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime
import datetime as dt

class Base(DeclarativeBase):
    pass

class Garage(Base):
    __tablename__ = 'garage'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    city = Column(String)
    capacity = Column(Integer)
    creationTime = Column(DateTime, default=dt.datetime.now)
    updateTime = Column(DateTime, onupdate=dt.datetime.now ,default=dt.datetime.now)


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    productionYear = Column(Integer)
    licensePlate = Column(String)
    garageIds = list[Garage]
    creationTime = Column(DateTime, default=dt.datetime.now)
    updateTime = Column(DateTime, onupdate=dt.datetime.now ,default=dt.datetime.now)
