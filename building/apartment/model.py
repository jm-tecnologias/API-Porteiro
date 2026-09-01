from datetime import datetime
from pydantic import BaseModel, Field


class ApartmentModel(BaseModel):
    id: int | None = Field(gt=0)
    floor: str | None = Field(min_length=2)
    number: str | None = Field(gt=0)
    type: str | None
    description: str = Field(min_length=100, max_length=1000)
    building_id: int
    status: bool
    created_at: datetime
    updated_at: datetime
