from datetime import date

from fastapi import APIRouter

from dtos.garage_dtos import ResponseGarageDTO, UpdateGarageDTO, CreateGarageDTO, GarageDailyAvailabilityReportDTO
from services.garage_service import get_garages, create_garage, delete_garage, get_garage, update_garage, \
     get_garage_daily_availability

garage_router = APIRouter()

# should be up here because if its below will match the get method
# of garages/{id} and it will interpret it like path param
@garage_router.get("/dailyAvailabilityReport", response_model=list[GarageDailyAvailabilityReportDTO])
async def get_daily_availability_report(garageId:int,startDate:date,endDate:date):
     return get_garage_daily_availability(garageId,startDate,endDate)

@garage_router.get("/{id}", response_model=ResponseGarageDTO)
async def get_single_garage(id: int):
     return get_garage(id)

@garage_router.get("/", response_model=list[ResponseGarageDTO])
async def get_all_garages_by_city(city: str | None = None):
     return get_garages(city=city)

@garage_router.post("/", response_model=ResponseGarageDTO)
async def create_new_garage(garage: CreateGarageDTO):
     return create_garage(garage)

@garage_router.put("/{id}", response_model=ResponseGarageDTO)
async def update_single_garage(id: int, garage: UpdateGarageDTO):
     return update_garage(id,garage)

@garage_router.delete("/{id}", response_model=bool)
async def delete_single_garage(id:int):
     return delete_garage(id)

