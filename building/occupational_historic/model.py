from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from building.apartment.model import ApartmentResponse


class HistoricModel(BaseModel):
    client_id: Optional[int] = None
    user_id: Optional[int] = None
    apartment_id: Optional[int] = None
    occupational_date: Optional[date] = None
    num_members: Optional[int] = None
    final_date: Optional[date] = None
    description: Optional[str] = None


class HistoricResponse(HistoricModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HistoricApartmentResponse(BaseModel):
    historic: HistoricResponse
    apartment: ApartmentResponse
