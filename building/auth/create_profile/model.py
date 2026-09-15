from datetime import datetime

from pydantic import BaseModel


class ProfileModel(BaseModel):
    profile: str | None = None
    description: str | None = None
    status: bool | None = None


class ProfileResponse(ProfileModel):
    id: int
    created_at: datetime
    updated_at: datetime
