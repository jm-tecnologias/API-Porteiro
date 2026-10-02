from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.check_in_out.member.dao import MemberCheckInOutDAO
from building.check_in_out.member.model import MemberCheckInOutModel, MemberCheckInOutResponse
from building.database.schemas import MemberCheckInOutSchema


class MemberCheckInOutService:
    def __init__(self, database: Session):
        self.dao = MemberCheckInOutDAO(database)

    def create(self, model: MemberCheckInOutModel) -> MemberCheckInOutResponse:
        # def create(self, user_token: str, member_token: str, model: MemberCheckInOutModel) ->
        # MemberCheckInOutResponse:

        new = MemberCheckInOutSchema(
            member_id=model.member_id,
            user_id=model.user_id,
            status=model.status,
            note=model.note
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data!')


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = MemberCheckInOutService(database)
#     data = MemberCheckInOutModel(
#         member_id=1,
#         user_id=1,
#         status="Check Out",
#         note="Check Out Test 587",
#     )
#     service.create(data)
#
# finally:
#     database.close()
