from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from building.apartment.model import ApartmentResponse
from building.client.model import ClientModel
from building.contact.model import ContactResponse
from building.rh.department.model import DepartmentResponse
from building.rh.employee.model import EmployeeResponse


class BuildingModel(BaseModel):
    name: str | None = None
    description: str | None = Field(min_length=10, max_length=1000)
    status: bool | None = None


class BuildingResponse(BuildingModel):
    id: int
    created_at: datetime
    updated_at: datetime
    contacts: list[ContactResponse] = Field(default_factory=list)
    departments: list[DepartmentResponse] = Field(default_factory=list)
    employees: list[EmployeeResponse] = Field(default_factory=list)
    apartments: list[ApartmentResponse] = Field(default_factory=True)
    clients: list[ClientModel] = Field(default_factory=True)
    model_config = ConfigDict(
        from_attributes=True
    )
