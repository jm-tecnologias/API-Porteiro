from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from building.check_in_out.visitor.model import VisitorCheckInOutResponse


class VisitorModel(BaseModel):
    member_id: Optional[int] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    visitor_date: Optional[date]
    visitor_time: Optional[time]
    status: Optional[str] = None
    description: Optional[str] = None
    barcode_url: Optional[str] = None


class VisitorResponse(VisitorModel):
    id: Optional[int] = None
    token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    visitor_check_historic: list[VisitorCheckInOutResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )
