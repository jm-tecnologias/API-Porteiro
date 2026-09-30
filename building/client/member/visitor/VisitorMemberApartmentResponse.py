from pydantic import BaseModel

from building.apartment.model import ApartmentResponse
from building.client.member.model import MemberResponse
from building.client.member.visitor.model import VisitorResponse


class VisitorMemberApartmentResponse(BaseModel):
    visitor: VisitorResponse
    member: MemberResponse
    apartment: ApartmentResponse
