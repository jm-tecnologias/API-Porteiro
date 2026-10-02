from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# class UserMemberModel(BaseModel):
#     username: Optional[str] = None
#     password: Optional[str] = None
#     description: Optional[str] = None
#     member_id: Optional[int] = None
#     status: Optional[bool] = None
#     profile_pic_url: Optional[str] = None


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


# class UserMemberResponse(UserMemberModel):
#     id: Optional[int] = None
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None
