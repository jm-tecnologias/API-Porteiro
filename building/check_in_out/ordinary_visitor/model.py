from datetime import datetime

from pydantic import BaseModel


class OrdinaryVisitorModel(BaseModel):
    member_id: int | None = None
    user_id: int | None = None
    name: str | None = None
    phone: str | None = None
    # 'Check In','Check Out'
    status: str | None = None
    description: str | None = None


class OrdinaryVisitorResponse(OrdinaryVisitorModel):
    id: int
    created_at: datetime
    updated_at: datetime
