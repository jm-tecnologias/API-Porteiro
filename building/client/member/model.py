from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from building.client.member.visitor.model import VisitorResponse


class MemberModel(BaseModel):
    user_id: int | None = None
    client_id: int | None = None
    apartment_id: int | None = None
    doc_id: str | None = None
    name: str | None = None
    surname: str | None = None
    phone: str | None = None
    email: str | None = None
    client_relationship: str | None = None
    description: str | None = None
    status: bool | None = None


class MemberResponse(MemberModel):
    id: int
    token: str
    created_at: datetime
    updated_at: datetime
    visitors: list[VisitorResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )
