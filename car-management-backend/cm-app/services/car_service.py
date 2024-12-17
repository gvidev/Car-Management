from dtos.car_dtos import CreateCarDTO, ResponseCarDTO
from repo.databaseConfig import Session
from sqlalchemy.orm import Session as ORMSession
from repo.models import Car
from services.garage_service import map_garage_to_response


def get_car_by_id(id:int):
    pass





def create_car(car: CreateCarDTO) -> ResponseCarDTO:
    newCar = map_create_to_car(car)
    with Session() as session:
        session.add(newCar)
        session.commit()
        session.refresh(newCar)
    return map_car_to_response(newCar)


def map_create_to_car(car: CreateCarDTO) -> Car:
    return Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
        garageIds = [map_garage_to_response(id) for id in ]
    )

def map_car_to_response(car: Car) -> ResponseCarDTO:
    return ResponseCarDTO(
        id=car.id,
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
    )