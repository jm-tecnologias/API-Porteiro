from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from building.address.model import AddressResponse
from building.apartment.model import ApartmentResponse
from building.auth.user.client.model import UserMemberResponse
from building.auth.user.client.service import UserMemberService
from building.barcode_service import BarcodeService
from building.client.member.MemberDashboardResponse import DashboardResponse
from building.client.member.dao import MemberDAO
from building.client.member.model import MemberResponse, MemberModel
from building.contact.model import ContactResponse
from building.database.schemas import MemberSchema
from building.model import BuildingResponse


class MemberService:
    def __init__(self, database: Session):
        self.dao = MemberDAO(database)
        self.user_member_service = UserMemberService(database)

    def create(self, model: MemberModel) -> MemberResponse:
        member = self.dao.find_by_name(model.name)
        if member:
            if member.surname == model.surname and member.status is True:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Member Already Exist!')
        new = MemberSchema(
            user_id=model.user_id,
            client_id=model.client_id,
            apartment_id=model.apartment_id,
            doc_id=model.doc_id,
            name=model.name,
            surname=model.surname,
            phone=model.phone,
            email=model.email,
            client_relationship=model.client_relationship,
            description=model.description,
            profile_pic_url=model.profile_pic_url
        )
        try:
            new_member = self.dao.create(new)
            if new_member:
                BarcodeService.generate_barcode('M', new_member.id)
            return new_member

        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data!')

    def update(self, member_id: int, member_data: MemberModel) -> MemberResponse:
        member = self.dao.find_by_id(member_id)
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

    def populate_dashboard(self, user_id: str, url_req: str) -> DashboardResponse:
        logged_user = self.user_member_service.verify_token(user_id)
        # Tratamento de erro se o login nao existir
        data = self.user_member_service.dao.load_dashboard(logged_user.id)
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
        user = self.user_member_service.verify_token(token)

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

    def list_all(self) -> list[MemberResponse]:
        return self.dao.find_all()


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = MemberService(database)
#     data = MemberModel(
#         user_id=1,
#         client_id=1,
#         doc_id="110100692835M",
#         apartment_id=1,
#         name="Teste",
#         surname="Mula",
#         phone="878201953",
#         email="email",
#         client_relationship="Filho",
#         description="Cliente membo de teste"
#     )
#     service.create(data)
#
# finally:
#     database.close()
