from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from dtos.car_dtos import CreateCarDTO, ResponseCarDTO, UpdateCarDTO
from repo.databaseConfig import Session
from sqlalchemy.orm import Session as ORMSession
from repo.models import Car
from services.garage_service import map_garage_to_response


class CarsFilter(BaseModel):
    carMake: Optional[str] = None
    garageId: Optional[int] = None
    fromYear: Optional[int] = None
    toYear: Optional[int] = None

def get_car_by_id(car_id:int, session: ORMSession):
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
        query =session.query(Car)
        if filters.carMake:
            query = query.filter(Car.make == filters.carMake)
        if filters.garageId:
            query = query.filter(Car.garageIds.any(id=filters.garageId))
        if filters.fromYear:
            query = query.filter(Car.productionYear >= filters.fromYear)
        if filters.toYear:
            query = query.filter(Car.productionYear <= filters.toYear)

        cars = query.all()
        response_cars = [map_car_to_response(car) for car in cars]
        return response_cars


def map_create_to_car(car: CreateCarDTO) -> Car:
    return Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
        # garageIds = [map_garage_to_response(id) for id in ]
    )

def map_car_to_response(car: Car) -> ResponseCarDTO:
    return ResponseCarDTO(
        id=car.id,
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
    )