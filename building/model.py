from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from building.apartment.model import ApartmentResponse
from building.client.model import ClientResponse, ClientWithMembersResponse
from building.contact.model import ContactResponse
from building.rh.department.model import DepartmentResponse
from building.rh.employee.model import EmployeeResponse


class BuildingModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class BuildingResponse(BuildingModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    contacts: Optional[list[ContactResponse]] = Field(default_factory=list)
    departments: Optional[list[DepartmentResponse]] = Field(default_factory=list)
    employees: Optional[list[EmployeeResponse]] = Field(default_factory=list)
    apartments: Optional[list[ApartmentResponse]] = Field(default_factory=list)
    # clients: Optional[list[ClientResponse]] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )


class BuildingResponseMoreDetails(BuildingResponse):
    # id: Optional[int] = None
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
    # contacts: Optional[list[ContactResponse]] = Field(default_factory=list)
    # departments: Optional[list[DepartmentResponse]] = Field(default_factory=list)
    # employees: Optional[list[EmployeeResponse]] = Field(default_factory=list)
    # apartments: Optional[list[ApartmentResponse]] = Field(default_factory=list)
    clients: Optional[list[ClientWithMembersResponse]] = Field(default_factory=list)
    # model_config = ConfigDict(
    #     from_attributes=True
    # )
