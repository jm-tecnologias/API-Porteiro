from datetime import datetime, date

from pydantic import BaseModel


class HistoricModel(BaseModel):
    client_id: int | None = None
    user_id: int | None = None
    apartment_id: int | None = None
    occupational_date: date | None = None
    num_members: int | None = 1
    final_date: date | None = None
    description: str | None = None


class HistoricResponse(HistoricModel):
    id: int
    created_at: datetime
    updated_at: datetime
