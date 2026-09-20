from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from building.client.member.model import MemberResponse
from building.occupational_historic.model import HistoricApartmentResponse, HistoricResponse


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
    members: list[MemberResponse] = Field(default_factory=list)
    historical: list[HistoricResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )
