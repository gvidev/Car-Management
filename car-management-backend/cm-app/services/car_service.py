from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from dtos.car_dtos import CreateCarDTO, ResponseCarDTO, UpdateCarDTO
from repo.databaseConfig import Session
from sqlalchemy.orm import Session as ORMSession
from repo.models import Car, Garage, CarGarage
from services.garage_service import map_garage_to_response, get_garage, get_garages_by_ids, get_garage_by_id


class CarsFilter(BaseModel):
    carMake: Optional[str] = None
    garageId: Optional[int] = None
    fromYear: Optional[int] = None
    toYear: Optional[int] = None

def get_car_by_id(car_id:int, session: ORMSession = None):
    if session is None:
        with Session() as session:
            car = session.get(Car, car_id)
            if car is None:
                raise HTTPException(status_code=404, detail="Car not found")
            return car
    else:
        car = session.get(Car, car_id)
        if car is None:
            raise HTTPException(status_code=404, detail="Car not found")
        return car


def get_car(car_id: int) -> ResponseCarDTO:
    with Session() as session:
        car = get_car_by_id(car_id,session)
        return map_car_to_response(car)

def update_car(car_id:int , car: UpdateCarDTO) -> ResponseCarDTO:
    with Session() as session:
        newCar = get_car_by_id(car_id,session)
        newCar.make = car.make
        newCar.model = car.model
        newCar.productionYear = car.productionYear
        newCar.licensePlate = car.licensePlate
        newCar.garages = get_garages_by_ids(car.garageIds,session)
        session.commit()
        session.refresh(newCar)

        return map_car_to_response(newCar)

def delete_car(car_id:int) -> bool:
    with Session() as session,session.begin():
        car = get_car_by_id(car_id,session)
        session.delete(car)
        return True

def create_car(car: CreateCarDTO) -> ResponseCarDTO:
    newCar = map_create_to_car(car)
    with Session() as session:
        session.add(newCar)
        session.commit()
        session.refresh(newCar)
    return map_car_to_response(newCar)


def get_cars(filters: CarsFilter) -> list[ResponseCarDTO]:
    with Session() as session:
        query = session.query(Car)
        if filters.carMake:
            search_car_make =f"%{filters.carMake.upper()}%"
            query = query.filter(Car.make.like(search_car_make))
        if filters.garageId:
            query = query.join(CarGarage).filter(CarGarage.garage_id == filters.garageId)
        if filters.fromYear:
            query = query.filter(Car.productionYear >= filters.fromYear)
        if filters.toYear:
            query = query.filter(Car.productionYear <= filters.toYear)

        cars = query.all()
        response_cars = [map_car_to_response(car) for car in cars]
        return response_cars


def map_create_to_car(car: CreateCarDTO) -> Car:
    newCar =  Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate
    )
    newCar.garages = get_garages_by_ids(garage_ids=car.garageIds)
    return newCar


def map_car_to_response(car: Car) -> ResponseCarDTO:
    return ResponseCarDTO(
        id=car.id,
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
        garages = [map_garage_to_response(garage) for garage in car.garages]
    )

