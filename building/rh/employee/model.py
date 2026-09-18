from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmployeeModel(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    description: Optional[str] = None
    building_id: Optional[int] = None
    status: Optional[bool] = None


class EmployeeResponse(EmployeeModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
