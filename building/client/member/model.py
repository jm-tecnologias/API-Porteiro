from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# from building.address.model import AddressResponse
# from building.apartment.model import ApartmentResponse
# from building.auth.user.client.model import UserMemberResponse
from building.client.member.visitor.model import VisitorResponse
# from building.contact.model import ContactResponse
# from building.model import BuildingResponse


class MemberModel(BaseModel):
    user_id: Optional[int] = None
    client_id: Optional[int] = None
    apartment_id: Optional[int] = None
    doc_id: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    client_relationship: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None
    profile_pic_url: Optional[str] = None
    barcode_url: Optional[str] = None


class MemberResponse(MemberModel):
    id: Optional[int] = None
    token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    visitors: list[VisitorResponse] = Field(default_factory=list)
    model_config = ConfigDict(
        from_attributes=True
    )



