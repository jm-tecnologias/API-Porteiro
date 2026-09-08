from datetime import datetime

from pydantic import BaseModel


class UserProfileModel(BaseModel):
    profile_id: int | None = None
    employee_user_id: int | None = None
    status: bool | None = None


class UserProfileResponse(UserProfileModel):
    id: int
    created_at: datetime
    updated_at: datetime
    