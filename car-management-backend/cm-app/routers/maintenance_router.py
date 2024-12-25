from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Query

from dtos.maintenance_dtos import ResponseMaintenanceDTO, UpdateMaintenanceDTO, CreateMaintenanceDTO, \
    MonthlyRequestsReportDTO
from services.maintenance_service import *


maintenance_router = APIRouter()

@maintenance_router.get("/monthlyRequestsReport", response_model=list[MonthlyRequestsReportDTO])
async def maintenance_monthly_requests_report(garageId:int,startMonth:str,endMonth:str):
     return get_maintenance_monthly_requests_report(garageId,startMonth,endMonth)

@maintenance_router.get("/{id}", response_model=ResponseMaintenanceDTO)
async def get_single_maintenance(id: int):
     return get_maintenance(id)

@maintenance_router.put("/{id}", response_model=ResponseMaintenanceDTO)
async def update_single_maintenance(id: int, maintenance: UpdateMaintenanceDTO):
     return update_maintenance(id,maintenance)

@maintenance_router.delete("/{id}", response_model=bool)
async def delete_single_maintenance(id:int):
     return delete_maintenance(id)

@maintenance_router.get("", response_model=list[ResponseMaintenanceDTO])
async def get_all_maintenances_by_filter(query_filters: Annotated[MaintenanceFilter,Query()]):
     return get_all_maintenances(query_filters)

@maintenance_router.post("", response_model=ResponseMaintenanceDTO)
async def create_new_maintenance(maintenance: CreateMaintenanceDTO):
     return create_maintenance(maintenance)


