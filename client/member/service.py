from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from building.address.model import AddressResponse
from building.apartment.model import ApartmentResponse
from client.auth.user.client.model import UserMemberResponse
from client.member.MemberDashboardResponse import DashboardResponse
from building.contact.model import ContactResponse
from building.model import BuildingResponse
from client.auth.user.client.dao import UserMemberDAO
from client.member.dao import MemberDAO
from client.member.model import MemberModel, MemberResponse
from utils.auth_service import AuthService


class MemberService:
    def __init__(self, database: Session):
        self.dao = MemberDAO(database)
        self.auth_helper = AuthService(database=database, model=UserMemberDAO)

    # def update(self, member_id: int, member_data: MemberModel) -> MemberResponse:
    #     member = self.dao.find_by_id(member_id)
    #     if not member:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member Not Found!')
    #     data = member_data.model_dump(exclude_unset=True)
    #     for field, value in data.items():
    #         setattr(member, field, value)
    #     try:
    #         return self.dao.update(member)
    #     except SQLAlchemyError:
    #         self.dao.rollback()
    #         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    #                             detail='Was Not Possible To Update Data!')

    def populate_dashboard(self, user_id: str, url_req: str) -> DashboardResponse:
        logged_user = self.auth_helper.verify_token(user_id)
        # Tratamento de erro se o login nao existir
        data = self.dao.load_dashboard(logged_user.id)
        if data is None:
            return None
        user, member, apartment, building, contact, address = data
        return DashboardResponse(
            user=UserMemberResponse(
                id=user.id,
                username=user.username,
                description=user.description,
                status=user.status
            ),
            member=MemberResponse(
                id=member.id,
                doc_id=member.doc_id,
                name=member.name,
                surname=member.surname,
                phone=member.phone,
                email=member.email,
                description=member.description,
                status=member.status,
                visitors=member.visitors,
                # barcode_url=url_req
                barcode_url=(url_req.rstrip('/') + f"/media/barcodes/M-{member.id:013d}.png")
            ),
            apartment=ApartmentResponse(
                id=apartment.id,
                floor=apartment.floor,
                number=apartment.number,
                type=apartment.type,
                description=apartment.description,
                status=apartment.status,
                occupation_state=apartment.occupation_state
            ),
            building=BuildingResponse(
                id=building.id,
                name=building.name,
                status=building.status,
                description=building.description
            ),
            contact=ContactResponse(
                id=contact.id,
                phone=contact.phone,
                email=contact.email,
                website=contact.website,
                status=contact.status
            ),
            address=AddressResponse(
                id=address.id,
                province=address.province,
                city=address.city,
                nearby_hood=address.nearby_hood,
                avenue=address.avenue,
                number=address.number,
                status=address.status
            )
        )

    def update_by_logged_client(self, token: str, member_data: MemberModel) -> MemberResponse:
        user = self.auth_helper.verify_token(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent Not Found!")

        member = self.dao.find_by_id(user.member_id)
        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member Not Found!')
        data = member_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(member, field, value)
        try:
            return self.dao.update(member)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Was Not Possible To Update Data!')
