from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.auth.user_profile.employee.dao import UserProfileDAO
from building.auth.user_profile.employee.model import UserProfileModel, UserProfileResponse
from building.database.schemas import UserProfileEmployeeSchema


class UserProfileService:
    def __init__(self, database: Session):
        self.dao = UserProfileDAO(database)

    def create(self, model: UserProfileModel) -> UserProfileResponse:
        user_profile = self.dao.check_user_profile(model.profile_id, model.employee_user_id)
        if user_profile:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Profile Already Given!')
        new = UserProfileEmployeeSchema(
            profile_id=model.profile_id,
            employee_user_id=model.employee_user_id
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data')

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = UserProfileService(database)
#     data = UserProfileModel(
#         profile_id=3,
#         employee_user_id=1,
#     )
#     service.create(data)
#
# finally:
#     database.close()
