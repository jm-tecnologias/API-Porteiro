from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserMemberModel(BaseModel):
    username: str | None = None
    password: str | None = None
    description: str | None = None
    member_id: int | None = None
    status: bool | None = None


class LoginResponse(BaseModel):
    id: int
    username: str
    description: str
    member_id: int
    status: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserMemberResponse(UserMemberModel):
    id: int
    created_at: datetime
    updated_at: datetime


class DashboardUserResponse(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class DashboardMemberResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    doc_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class DashboardApartmentResponse(BaseModel):
    id: Optional[int] = None
    floor: Optional[str] = None
    number: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    occupation_state: Optional[str] = None
    status: Optional[bool] = None


class DashboardBuildingResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


class DashboardContactResponse(BaseModel):
    id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    status: Optional[bool] = None


class DashboardAddressResponse(BaseModel):
    id: Optional[int] = None
    province: Optional[str] = None
    city: Optional[str] = None
    nearby_hood: Optional[str] = None
    avenue: Optional[str] = None
    number: Optional[str] = None
    status: Optional[bool] = None


class DashboardResponse(BaseModel):
    user: DashboardUserResponse
    member: DashboardMemberResponse
    apartment: DashboardApartmentResponse
    building: DashboardBuildingResponse
    contact: DashboardContactResponse
    address: DashboardAddressResponse
