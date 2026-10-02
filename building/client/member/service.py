from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from building.apartment.model import ApartmentResponse
from building.barcode_service import BarcodeService
from building.client.member.MemberApartmentResponse import MemberApartmentResponse
from building.client.member.dao import MemberDAO
from building.client.member.model import MemberResponse, MemberModel
from building.database.schemas import MemberSchema


class MemberService:
    def __init__(self, database: Session):
        self.dao = MemberDAO(database)

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

    def scan_member(self, member_id: int) -> MemberApartmentResponse:
        data = self.dao.find_member(member_id)
        me, ap = data
        return MemberApartmentResponse(
            member=MemberResponse(
                user_id=me.user_id,
                client_id=me.client_id,
                apartment_id=me.apartment_id,
                doc_id=me.doc_id,
                name=me.name,
                surname=me.surname,
                phone=me.phone,
                email=me.email,
                client_relationship=me.client_relationship,
                description=me.description,
                status=me.status,
                profile_pic_url=me.profile_pic_url,
                # barcode_url
                id=me.id,
                token=me.token,
                created_at=me.created_at,
                updated_at=me.updated_at,
                visitors=me.visitors,
                checkedStatus=me.checkedStatus
            ),
            apartment=ApartmentResponse(
                floor=ap.floor,
                number=ap.number,
                type=ap.type,
                description=ap.description,
                occupation_state=ap.occupation_state,
                building_id=ap.building_id,
                status=ap.status,
                id=ap.id,
                created_at=ap.created_at,
                updated_at=ap.updated_at
            )
        )


# from utils.database import SessionLocal
# from building.database import models
#
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

    # member = service.find_member(1)
    # me, ap = member
    # print('Member: ', me)
    # print('Apartment: ', ap)

# finally:
#     database.close()
