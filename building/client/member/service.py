from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
            description=model.description
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data!')

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
