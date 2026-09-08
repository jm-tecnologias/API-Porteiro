from datetime import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    user_id: int | None = None
    surname: str | None = None
    num_members: int | None = None
    description: str | None = None
    building_id: int | None = None
    status: bool | None = None


class ClientResponse(ClientModel):
    id: int
    created_at: datetime
    updated_at: datetime
