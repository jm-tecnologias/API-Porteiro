from datetime import datetime, date, time

from pydantic import BaseModel, ConfigDict, Field


class VisitorCheckInOutModel(BaseModel):
    visitor_id: int | None = None
    user_id: int | None = None
    status: str | None = None
    note: str | None = None


class VisitorCheckInOutResponse(VisitorCheckInOutModel):
    created_at: datetime

