from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class DepartmentModel(BaseModel):
    id: int | None = Field(gt=0)
    code: str = Field(min_length=3)
    name: str = Field(min_length=2)
    description: str = Field(min_length=10, max_length=1000)
    building_id: int
    status: bool | None = True
    created_at: datetime
    updated_at: datetime

