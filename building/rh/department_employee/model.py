from datetime import date, datetime

from pydantic import BaseModel


class DepEmpModel(BaseModel):
    department_id: int | None = None
    employee_id: int | None = None
    position: str | None = None
    initial_date: date | None = None
    final_date: date | None = None
    description: str | None = None
    status: bool | None = None


class DepEmpResponse(DepEmpModel):
    created_at: datetime
    updated_at: datetime
