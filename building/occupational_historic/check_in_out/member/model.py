from datetime import datetime
from pydantic import BaseModel


class MemberCheckInOutModel(BaseModel):
    member_id: int | None = None
    user_id: int | None = None
    status: str | None = None
    note: str | None = None


class MemberCheckInOutResponse(MemberCheckInOutModel):
    created_at: datetime
    updated_at: datetime
    