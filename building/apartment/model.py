from datetime import datetime
from pydantic import BaseModel


class ApartmentModel(BaseModel):
    floor: str | None = None
    number: str | None = None
    type: str | None = None
    description: str | None = None
    occupation_state: str | None = None
    building_id: int | None = None
    status: bool | None = None


class ApartmentResponse(ApartmentModel):
    id: int
    created_at: datetime
    updated_at: datetime
