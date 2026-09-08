from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.client.member.dao import MemberDAO
from building.client.member.model import MemberResponse, MemberModel
from building.database.schemas import MemberSchema


class MemberService:
    def __init__(self, database: Session):
        self.dao = MemberDAO(database)

    def create(self, model: MemberModel) -> MemberResponse:
        member = self.dao.find_by_phone(model.name)
        if member:
            if member.surname == model.surname and member.status is True:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Member Already Exist!')
        new = MemberSchema(
            user_id=model.user_id,
            client_id=model.client_id,
            doc_id=model.doc_id,
            name=model.name,
            surname=model.surname,
            phone=model.phone,
            email=model.email,
            description=model.description
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data!')


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = MemberService(database)
#     data = MemberModel(
#         user_id=1,
#         client_id=1,
#         doc_id="110100692835M",
#         name="Junior",
#         surname="Mula",
#         phone="878201993",
#         email="email",
#         description="Cliente membo de teste"
#     )
#     service.create(data)
#
# finally:
#     database.close()
