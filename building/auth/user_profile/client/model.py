from datetime import datetime

from pydantic import BaseModel


class UserProfileMemberModel(BaseModel):
    profile_id: int | None = None
    member_user_id: int | None = None
    status: bool | None = None


class UserProfileMemberResponse(UserProfileMemberModel):
    id: int
    created_at: datetime
    updated_at: datetime
