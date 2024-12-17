
from pydantic import BaseModel, Field

from dtos.garage_dtos import ResponseGarageDTO

class CreateCarDTO(BaseModel):
    make:str = Field(None)
    model:str = Field(None)
    productionYear: int = Field(None)
    licensePlate:str = Field(None)
    garageIds:list[int] = Field(None)

class UpdateCarDTO(BaseModel):
    make:str = Field(None)
    model:str = Field(None)
    productionYear: int = Field(None)
    licensePlate:str = Field(None)
    garageIds:list[int] = Field(None)

class ResponseCarDTO(BaseModel):
    id:int
    make:str
    model:str
    productionYear: int
    licensePlate:str
    garages:list[ResponseGarageDTO]