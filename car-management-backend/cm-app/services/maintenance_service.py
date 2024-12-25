from calendar import isleap
from datetime import date, datetime, timedelta
from typing import Optional

from dns.e164 import query
from fastapi import HTTPException
from httpcore import request
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session as ORMSession

from dtos.maintenance_dtos import ResponseMaintenanceDTO, UpdateMaintenanceDTO, CreateMaintenanceDTO, \
    MonthlyRequestsReportDTO, YearMonth
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



def get_maintenance_monthly_requests_report(garageId:int,startMonth:str,endMonth:str)\
        -> list[MonthlyRequestsReportDTO]:
    startMonth = datetime.strptime(startMonth, "%Y-%m").date()
    endMonth = (datetime.strptime(endMonth, "%Y-%m") + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    endMonth = endMonth.date()
    with Session() as session:
        #query that get count of request per month
        results = (
            session.query(
                func.strftime('%Y-%m', Maintenance.scheduledDate).label("year_month"),
                func.count(Maintenance.id).label("requests"),
            ).filter(
                Maintenance.garage_id == garageId,
                func.date(Maintenance.scheduledDate) >= startMonth,
                func.date(Maintenance.scheduledDate) <= endMonth,
            ).group_by(func.strftime('%Y-%m', Maintenance.scheduledDate))
             .order_by(func.strftime('%Y-%m', Maintenance.scheduledDate))
            .all()
        )

        if not results:
            raise HTTPException(status_code=404, detail="No results")

        monthly_requests_report = []
        # going from start month to end month
        current_month = startMonth
        while current_month <= endMonth:
            is_found = False

            for result in results:
                year_month = result.year_month
                if current_month.strftime('%Y-%m') == year_month:
                    monthly_requests_report.append(
                        MonthlyRequestsReportDTO(
                            yearMonth=YearMonth(
                                year=current_month.year,
                                month=current_month.strftime("%B").upper(),
                                leapYear=isleap(current_month.year),
                                monthValue=current_month.month,
                            ),
                            requests = result.requests
                        ))

                    is_found = True
                    break

            if not is_found:
                monthly_requests_report.append(MonthlyRequestsReportDTO(
                            yearMonth=YearMonth(
                                year=current_month.year,
                                month=current_month.strftime("%B").upper(),
                                leapYear=isleap(current_month.year),
                                monthValue=current_month.month,
                            ),
                            requests = 0
                        ))

            if current_month.month < 12:
                current_month = current_month.replace(month=current_month.month + 1)
            else:
                current_month = current_month.replace(year=current_month.year + 1, month=1)

        return monthly_requests_report


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