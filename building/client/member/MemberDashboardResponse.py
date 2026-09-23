from pydantic import BaseModel

from building.address.model import AddressResponse
from building.apartment.model import ApartmentResponse
from building.auth.user.client.model import UserMemberResponse
from building.client.member.model import MemberResponse
from building.contact.model import ContactResponse
from building.model import BuildingResponse


class DashboardResponse(BaseModel):
    user: UserMemberResponse
    member: MemberResponse
    apartment: ApartmentResponse
    building: BuildingResponse
    contact: ContactResponse
    address: AddressResponse
