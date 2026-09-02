from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


class AddressModel(BaseModel):
    province: str | None = None
    city: str | None = None
    nearby_hood: str | None = None
    avenue: str | None = None
    number: int | None = None
    building_id: int | None = None
    status: bool | None = None


class AddressResponse(AddressModel):
    id: int
    created_at: datetime
    updated_at: datetime
