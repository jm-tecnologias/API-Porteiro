from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str | None = None
    password: str | None = None
    description: str | None = None
    employee_id: int | None = None
    # profile_id: int | None = None
    status: bool | None = None


class UserResponse(UserModel):
    id: int
    created_at: datetime
    updated_at: datetime
