from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel


class DepartmentModel(BaseModel):
    code: str | None = None
    name: str | None = None
    description: str | None = None
    building_id: int | None = None
    status: bool | None = None


class DepartmentResponse(DepartmentModel):
    id: int
    created_at: datetime
    updated_at: datetime

