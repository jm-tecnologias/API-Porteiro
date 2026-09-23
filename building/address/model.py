from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddressModel(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    nearby_hood: Optional[str] = None
    avenue: Optional[str] = None
    number: Optional[int] = None
    building_id: Optional[int] = None
    status: Optional[bool] = None


class AddressResponse(AddressModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
