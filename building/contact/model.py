from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContactModel(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    building_id: Optional[int] = None
    status: Optional[bool] = None


class ContactResponse(ContactModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
