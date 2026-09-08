from datetime import datetime

from pydantic import BaseModel


class PermissionModel(BaseModel):
    module: str | None = None
    action: str | None = None
    code: str | None = None
    status: bool | None = None


class PermissionResponse(PermissionModel):
    id: int
    created_at: datetime
    updated_at: datetime
