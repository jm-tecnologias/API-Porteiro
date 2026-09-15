from datetime import datetime

from pydantic import BaseModel


class UserProfileEmployeeModel(BaseModel):
    profile_id: int | None = None
    employee_user_id: int | None = None
    status: bool | None = None


class UserProfileEmployeeResponse(UserProfileEmployeeModel):
    id: int
    created_at: datetime
    updated_at: datetime
