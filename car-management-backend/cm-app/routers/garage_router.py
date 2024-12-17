from datetime import date
from xmlrpc.client import boolean, Boolean

from fastapi import APIRouter

from dtos import GarageResponse, GarageRequest
from models import Garage
from services.garage_service import get_garages, create_garage, delete_garage, get_garage, update_garage, \
     get_garage_daily_availability

garage_router = APIRouter()

@garage_router.get("/{id}", response_model=GarageResponse)
async def get_single_garage(id: int):
     return get_garage(id)

@garage_router.get("/", response_model=list[GarageResponse])
async def get_all_garages_by_city(city: str | None = None):
     return get_garages(city=city)

@garage_router.post("/", response_model=GarageResponse)
async def create_new_garage(garage: GarageRequest):
     return create_garage(garage)

@garage_router.put("/{id}", response_model=GarageResponse)
async def update_single_garage(id: int, garage: GarageRequest):
     return update_garage(id,garage)

@garage_router.delete("/{id}", response_model=bool)
async def delete_single_garage(id:int):
     return delete_garage(id)

@garage_router.get("/dailyAvailabilityReport")
async def get_daily_availability_report(garageId:int,startDate:date,endDate:date):
     return get_garage_daily_availability(garageId,startDate,endDate)