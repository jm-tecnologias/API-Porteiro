from datetime import datetime

from pydantic import BaseModel


class UserEmployeeModel(BaseModel):
    username: str | None = None
    password: str | None = None
    description: str | None = None
    employee_id: int | None = None
    # profile_id: int | None = None
    status: bool | None = None


class LoginResponse(BaseModel):
    id: int
    username: str
    description: str
    member_id: int
    status: bool
    created_at: datetime
    updated_at: datetime


class UserEmployeeResponse(UserEmployeeModel):
    id: int
    created_at: datetime
    updated_at: datetime
