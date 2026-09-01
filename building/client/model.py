from datetime import datetime

from pydantic import BaseModel, Field


class ClientModel(BaseModel):
    id: int | None = Field(gt=0)
    user_id: int = Field(gt=0)
    surname: str = Field(min_length=2)
    num_members: int = Field(gt=0)
    description: str = Field(min_length=100, max_length=1000)
    building_id: int
    status: bool
    created_at: datetime
    updated_at: datetime