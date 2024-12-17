from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ResponseGarageDTO(BaseModel):
    id: int
    name:str
    location: str
    city: str
    capacity: int

class CreateGarageDTO(BaseModel):
    name:str
    location:str
    city:str
    capacity:int

class UpdateGarageDTO(BaseModel):
    name: str = Field(None)
    location: str = Field(None)
    city: str = Field(None)
    capacity: int = Field(None)

class GarageDailyAvailabilityReportDTO(BaseModel):
    date: datetime
    requests: int
    availableCapacity:int