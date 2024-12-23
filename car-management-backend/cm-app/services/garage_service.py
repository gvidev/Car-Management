from datetime import date

from fastapi import HTTPException

from repo.databaseConfig import Session
from dtos.garage_dtos import ResponseGarageDTO, UpdateGarageDTO, CreateGarageDTO, GarageDailyAvailabilityReportDTO
from repo.models import Garage
from sqlalchemy.orm import Session as ORMSession

def get_garages_by_ids(garage_ids:list[int],outer_session:ORMSession = None)\
        -> list[Garage]:
    if outer_session is None:
        with Session() as session:
            return session.query(Garage).filter(Garage.id.in_(garage_ids)).all()
    else:
        return outer_session.query(Garage).filter(Garage.id.in_(garage_ids)).all()

def get_garage_by_id(id:int, session: ORMSession = None):
    if session is None:
        with Session() as session:
            garage = session.get(Garage, id)
            if garage is None:
                raise HTTPException(status_code=404, detail="Garage not found!")
            return garage
    else:
        garage = session.get(Garage, id)
        if garage is None:
            raise HTTPException(status_code=404, detail="Garage not found!")
        return garage

def get_garage(id: int) ->ResponseGarageDTO:
    with Session() as session, session.begin():
        garage = get_garage_by_id(id, session)
        return map_garage_to_response(garage)

def get_garages(city: str | None = None) -> list[ResponseGarageDTO]:
    with Session() as session:
        if city:
            search_city = f"%{city}%"
            garages = session.query(Garage) \
            .where(Garage.city.ilike(search_city)).all()
        else:
            garages = session.query(Garage).all()

        return [map_garage_to_response(garage) for garage in garages]


def update_garage(id: int,
                  garage:UpdateGarageDTO) -> ResponseGarageDTO:
    with Session() as session:
        newGarage = get_garage_by_id(id, session)
        newGarage.city = garage.city
        newGarage.location = garage.location
        newGarage.capacity = garage.capacity
        newGarage.name = garage.name

        session.commit()
        session.refresh(newGarage)
        return map_garage_to_response(newGarage)


def create_garage(garage: CreateGarageDTO) -> ResponseGarageDTO:
    newGarage = map_create_to_garage(garage)
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

def get_garage_daily_availability(garage_id:int, start_date:date, end_date:date)\
        -> GarageDailyAvailabilityReportDTO:
    with Session() as session:
        garage = get_garage_by_id(garage_id, session)
        pass


def map_garage_to_response(garage: Garage) -> ResponseGarageDTO:
    return ResponseGarageDTO(
        id=garage.id,
        name=garage.name,
        location=garage.location,
        capacity=garage.capacity,
        city=garage.city,
    )

def map_update_to_garage(garage: UpdateGarageDTO) -> Garage:
    return Garage(
        name = garage.name,
        location = garage.location,
        capacity = garage.capacity,
        city = garage.city
    )

def map_create_to_garage(garage: UpdateGarageDTO) -> Garage:
    return Garage(
        name = garage.name,
        location = garage.location,
        capacity = garage.capacity,
        city = garage.city
    )