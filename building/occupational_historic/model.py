from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class HistoricModel(BaseModel):
    client_id: int | None = None
    user_id: int | None = None
    apartment_id: int | None = None
    occupational_date: date | None = None
    num_members: int | None = 1
    final_date: date | None = None
    description: str | None = None


class HistoricResponse(HistoricModel):
    id: int
    created_at: datetime
    updated_at: datetime


class Historic(BaseModel):
    client_id: Optional[int] = None
    apartment_id: Optional[int] = None
    occupational_date: Optional[date] = None
    final_date: Optional[date] = None
    description: Optional[str] = None


class Apartment(BaseModel):
    id: Optional[int] = None
    floor: Optional[str] = None
    number: Optional[str] = None
    type: Optional[str] = None
    occupation_state: Optional[str] = None
    description: Optional[str] = None


class HistoricApartmentResponse(BaseModel):
    historic: Historic
    apartment: Apartment
