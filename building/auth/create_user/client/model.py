from datetime import datetime
from pydantic import BaseModel


class UserMemberModel(BaseModel):
    username: str | None = None
    password: str | None = None
    description: str | None = None
    member_id: int | None = None
    status: bool | None = None


class UserMemberResponse(UserMemberModel):
    id: int
    created_at: datetime
    updated_at: datetime
