from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


class ContactModel(BaseModel):
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    building_id: int | None = None
    status: bool | None = None


class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime
