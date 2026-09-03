from datetime import datetime
from pydantic import BaseModel


class EmployeeModel(BaseModel):
    code: str | None = None
    name: str | None = None
    surname: str | None = None
    description: str | None = None
    building_id: int | None = None
    status: bool | None = None


class EmployeeResponse(EmployeeModel):
    id: int
    created_at: datetime
    updated_at: datetime
