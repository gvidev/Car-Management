from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime
import datetime as dt

class Base(DeclarativeBase):
    pass

# using index=True we optimise the search time when filter by column

class Garage(Base):
    __tablename__ = 'garage'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    city = Column(String, index=True)
    capacity = Column(Integer)
    creationTime = Column(DateTime, default=dt.datetime.now)
    updateTime = Column(DateTime, onupdate=dt.datetime.now ,default=dt.datetime.now)


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String)
    productionYear = Column(Integer, index=True)
    licensePlate = Column(String)
    garageIds = list[Garage]
    creationTime = Column(DateTime, default=dt.datetime.now)
    updateTime = Column(DateTime, onupdate=dt.datetime.now ,default=dt.datetime.now)
