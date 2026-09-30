from pydantic import BaseModel

from building.apartment.model import ApartmentResponse
from building.client.member.model import MemberResponse


class MemberApartmentResponse(BaseModel):
    member: MemberResponse
    apartment: ApartmentResponse
