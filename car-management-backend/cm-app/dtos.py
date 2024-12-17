from datetime import datetime

from pydantic import BaseModel, Field


class GarageResponse(BaseModel):
    id: int
    name:str
    location: str
    city: str
    capacity: int

class GarageRequest(BaseModel):
    name:str
    location:str
    city:str
    capacity:int
