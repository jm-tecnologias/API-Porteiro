from datetime import datetime
from pydantic import BaseModel


class ProfilePermissionModel(BaseModel):
    profile_id: int | None = None
    permission_id: int | None = None
    status: bool | None = None


class ProfilePermissionResponse(ProfilePermissionModel):
    id: int
    created_at: datetime
    updated_at: datetime
