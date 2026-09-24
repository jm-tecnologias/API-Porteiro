from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VisitorCheckInOutModel(BaseModel):
    visitor_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None
    note: Optional[str] = None


class VisitorCheckInOutResponse(VisitorCheckInOutModel):
    created_at: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True
    )
