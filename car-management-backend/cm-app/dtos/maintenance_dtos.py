from datetime import date, datetime

from pydantic import BaseModel, Field


class CreateMaintenanceDTO(BaseModel):
    garageId: int
    carId: int
    serviceType: str
    scheduledDate: date

class UpdateMaintenanceDTO(BaseModel):
    carId:int = Field(None)
    serviceType:str = Field(None)
    scheduledDate:date = Field(None)
    garageId:int

class ResponseMaintenanceDTO(BaseModel):
     id:int = Field(None)
     carId:int = Field(None)
     carName:str = Field(None)
     serviceType:str = Field(None)
     scheduledDate:date = Field(None)
     garageId:int = Field(None)
     garageName:str = Field(None)


class MonthlyRequestsReportDTO(BaseModel):
     yearMonth:list = Field(None)
     requests:int = Field(None)