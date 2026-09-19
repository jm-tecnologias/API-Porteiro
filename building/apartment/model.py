from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ApartmentModel(BaseModel):
    floor: Optional[str] = None
    number: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    occupation_state: Optional[str] = None
    building_id: Optional[int] = None
    status: Optional[bool] = None


class ApartmentResponse(ApartmentModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
