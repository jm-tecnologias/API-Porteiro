import datetime
from _pydatetime import datetime
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from building.client.member.model import MemberResponse
from building.occupational_historic.model import HistoricResponse


class ClientModel(BaseModel):
    user_id: Optional[int] = None
    surname: Optional[str] = None
    num_members: Optional[int] = None
    description: Optional[str] = None
    building_id: Optional[int] = None
    status: Optional[bool] = None


class ClientResponse(ClientModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    historical: list[HistoricResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )


class ClientWithMembersResponse(ClientResponse):
    members: list[MemberResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )
