from fastapi import APIRouter

from dtos.car_dtos import ResponseCarDTO, CreateCarDTO

car_router  = APIRouter()

@car_router.post("/", response_model=ResponseCarDTO)
async def create_new_car(car: CreateCarDTO):
     return create_car(car)


