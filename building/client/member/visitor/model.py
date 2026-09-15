from datetime import datetime, date, time

from pydantic import BaseModel, ConfigDict, Field

from building.client.check_in_out.visitor.model import VisitorCheckInOutResponse


class VisitorModel(BaseModel):
    member_id: int | None = None
    name: str | None = None
    phone: str | None = None
    date: date
    time: time
    status: str | None = None
    description: str | None = None


class VisitorResponse(VisitorModel):
    id: int
    token: str
    created_at: datetime
    updated_at: datetime
    visitor_check_historic: list[VisitorCheckInOutResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )
