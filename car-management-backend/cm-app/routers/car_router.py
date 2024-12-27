from typing import Annotated

from fastapi import APIRouter,Query
from httpx import QueryParams

from dtos.car_dtos import ResponseCarDTO, CreateCarDTO, UpdateCarDTO
from http_responses import responses
from services.car_service import get_car, update_car, delete_car, get_cars, create_car, CarsFilter

car_router  = APIRouter()


@car_router.get("/{id}", response_model=ResponseCarDTO, responses=responses)
async def get_single_car(id: int):
     return get_car(id)

@car_router.put("/{id}", response_model=ResponseCarDTO,responses=responses)
async def update_single_car(id: int, car: UpdateCarDTO):
     return update_car(id, car)

@car_router.delete("/{id}", response_model=bool,responses=responses)
async def delete_single_car(id: int):
     return delete_car(id)

@car_router.get("", response_model=list[ResponseCarDTO],responses=responses)
async def get_all_cars(query_filters: Annotated[CarsFilter,Query()]):
     return get_cars(query_filters)

@car_router.post("", response_model=ResponseCarDTO,responses=responses)
async def create_new_car(car: CreateCarDTO):
     return create_car(car)



