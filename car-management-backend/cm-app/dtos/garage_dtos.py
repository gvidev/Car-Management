from datetime import date

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
    reportDate:date = Field(None, alias="date") # Using 'date' as the field name needs to be with alias
    # or it will return FieldInfo build error because the 'date' is used by pydantic
    requests: int = Field(None)
    availableCapacity:int = Field(None)
