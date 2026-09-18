from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from building.rh.employee.model import EmployeeResponse


class UserEmployeeModel(BaseModel):
    username: str | None = None
    password: str | None = None
    description: str | None = None
    employee_id: int | None = None
    # profile_id: int | None = None
    status: bool | None = None


class ModelLogin(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    description: Optional[str] = None
    employee_id: Optional[int] = None
    status: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserEmployee(BaseModel):
    user: ModelLogin
    employee: EmployeeResponse


class UserEmployeeResponse(UserEmployeeModel):
    id: int
    created_at: datetime
    updated_at: datetime
