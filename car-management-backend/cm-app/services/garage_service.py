from datetime import date

from fastapi import HTTPException

from databaseConfig import Session
from dtos import GarageResponse, GarageRequest
from models import Garage
from sqlalchemy.orm import Session as ORMSession


def get_garage_by_id(id:int, session: ORMSession):
    garage = session.get(Garage,id)
    if garage is None:
        raise HTTPException(status_code=404, detail="Garage not found!")
    return garage

def get_garage(id: int) ->GarageResponse:
    with Session() as session, session.begin():
        garage = get_garage_by_id(id, session)
        return map_garage_to_response(garage)

def get_garages(city: str | None = None) -> list[GarageResponse]:
    with Session() as session:
        if city:
            search_city = f"%{city}%"
            garages = session.query(Garage) \
            .where(Garage.city.ilike(search_city)).all()
        else:
            garages = session.query(Garage).all()

        return [map_garage_to_response(garage) for garage in garages]


def update_garage(id: int, garage:GarageRequest) -> GarageResponse:
    with Session() as session:
        newGarage = get_garage_by_id(id, session)
        newGarage.city = garage.city
        newGarage.location = garage.location
        newGarage.capacity = garage.capacity
        newGarage.name = garage.name
        session.commit()
        session.refresh(newGarage)
        return map_garage_to_response(newGarage)


def create_garage(garage: GarageRequest) -> GarageResponse:
    newGarage = map_request_to_paste(garage)
    with Session() as session:
        session.add(newGarage)
        session.commit()
        session.refresh(newGarage)
        return map_garage_to_response(newGarage)

def delete_garage(id: int) -> bool:
    with Session() as session, session.begin():
        garage = get_garage_by_id(id, session)
        session.delete(garage)
        return True

def get_garage_daily_availability(garage_id:int, start_date:date, end_date:date):
    pass

def map_garage_to_response(garage: Garage) -> GarageResponse:
    return GarageResponse(
        id=garage.id,
        name=garage.name,
        location=garage.location,
        capacity=garage.capacity,
        city=garage.city,
    )

def map_request_to_paste(garage: GarageRequest) -> Garage:
    return Garage(
        name = garage.name,
        location = garage.location,
        capacity = garage.capacity,
        city = garage.city
    )