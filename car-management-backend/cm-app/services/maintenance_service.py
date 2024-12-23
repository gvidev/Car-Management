from datetime import date
from typing import Optional

from dns.e164 import query
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session as ORMSession

from dtos.maintenance_dtos import ResponseMaintenanceDTO, UpdateMaintenanceDTO, CreateMaintenanceDTO
from repo.databaseConfig import Session
from repo.models import Maintenance
from services.car_service import get_car_by_id
from services.garage_service import get_garage_by_id


class MaintenanceFilter(BaseModel):
    carId: Optional[int] = None
    garageId: Optional[int] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None

def get_maintenance_by_id(id:int, session:ORMSession):
    maintenance = session.get(Maintenance, id)
    if maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance

def get_maintenance(id:int) -> ResponseMaintenanceDTO:
    with Session() as session:
        maintenance = get_maintenance_by_id(id, session)
        return map_maintenance_to_response(maintenance)

def update_maintenance(id:int,update_mt:UpdateMaintenanceDTO)\
        -> ResponseMaintenanceDTO:
    with Session() as session:
        isFull = is_garage_spaces_full(update_mt.garageId, update_mt.scheduledDate, session)
        if isFull:
            raise HTTPException(status_code=304, detail="Garage is full on this date")
        newMt = get_maintenance_by_id(id, session)
        newMt.car_id = update_mt.carId
        newMt.garage_id = update_mt.garageId
        newMt.serviceType = update_mt.serviceType
        newMt.scheduledDate = update_mt.scheduledDate
        session.commit()
        session.refresh(newMt)

        return map_maintenance_to_response(newMt)

def delete_maintenance(id:int):
    with Session() as session:
        maintenance = get_maintenance_by_id(id, session)
        session.delete(maintenance)
        session.commit()



def get_all_maintenances(filters: MaintenanceFilter) \
    -> list[ResponseMaintenanceDTO]:
    with Session() as session:
        query = session.query(Maintenance)
        if filters.carId:
            query = query.filter(Maintenance.car_id == filters.carId)
        if filters.garageId:
            query = query.filter(Maintenance.garage_id == filters.garageId)
        if filters.startDate:
            query = query.filter(Maintenance.scheduledDate.date() >= filters.startDate)
        if filters.endDate:
            query = query.filter(Maintenance.scheduledDate.date() <= filters.endDate)

        maintenances = query.all()
        response_maintenances = \
         [map_maintenance_to_response(mt) for mt in maintenances]
        return response_maintenances


def create_maintenance(maintenance: CreateMaintenanceDTO)\
        -> ResponseMaintenanceDTO:
    new_maintenance = map_create_to_maintenance(maintenance)
    with Session() as session:
        isFull = is_garage_spaces_full(new_maintenance.garage_id, new_maintenance.scheduledDate, session)
        if isFull:
            raise HTTPException(status_code=304, detail="Garage is full on this date")
        session.add(new_maintenance)
        session.commit()
        session.refresh(new_maintenance)
        return map_maintenance_to_response(new_maintenance)


def maintenances_with_start_to_end_date(start_date, end_date, garage_id, session):
    query = session.query(Maintenance)
    query = query.filter(Maintenance.scheduledDate.date() >= start_date)
    query = query.filter(Maintenance.scheduledDate.date() <= end_date)
    query = query.filter(Maintenance.garage_id == garage_id)
    maintenances = query.all()
    return maintenances

def get_maintenance_monthly_requests_report(garageId,startMonth,endMonth):
    pass


def is_garage_spaces_full(garage_id:int, scheduled_date:date, session:ORMSession) -> bool:
    garage = get_garage_by_id(garage_id, session)
    garage_capacity = garage.capacity
    request_garages = session.query(Maintenance)\
                                     .filter(Maintenance.garage_id== garage_id).all()
    requests_garage_by_date = []
    for request in request_garages:
        if request.scheduledDate.date() == scheduled_date:
            requests_garage_by_date.append(request)



    if garage_capacity - len(requests_garage_by_date) > 0:
        return False

    return True


def map_create_to_maintenance(mt: CreateMaintenanceDTO)->Maintenance:
    return Maintenance(
    serviceType = mt.serviceType,
    scheduledDate = mt.scheduledDate ,
    car_id = mt.carId ,
    garage_id = mt.garageId
    )


def map_maintenance_to_response(mt: Maintenance) -> ResponseMaintenanceDTO:
    return ResponseMaintenanceDTO(
        id = mt.id,
        carId = mt.car_id,
        carName = get_car_by_id(mt.car_id).make,
        serviceType = mt.serviceType,
        scheduledDate = mt.scheduledDate,
        garageId = mt.garage_id,
        garageName = get_garage_by_id(mt.garage_id).name
    )