from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.auth.user_profile.client.dao import UserProfileMemberDAO
from building.auth.user_profile.client.model import UserProfileMemberModel, UserProfileMemberResponse
from building.database.schemas import UserProfileMemberSchema


class UserProfileMemberService:
    def __init__(self, database: Session):
        self.dao = UserProfileMemberDAO(database)

    def create(self, model: UserProfileMemberModel) -> UserProfileMemberResponse:
        user_profile = self.dao.check_user_profile(model.profile_id, model.member_user_id)
        if user_profile:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Profile Already Given!')
        new = UserProfileMemberSchema(
            profile_id=model.profile_id,
            member_user_id=model.member_user_id
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data')

from utils.database import SessionLocal
from building.database import models
database = SessionLocal()
try:
    service = UserProfileMemberService(database)
    data = UserProfileMemberModel(
        profile_id=2,
        member_user_id=1,
    )
    service.create(data)

finally:
    database.close()
