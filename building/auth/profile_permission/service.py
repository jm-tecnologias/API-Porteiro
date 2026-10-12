from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from building.database.schemas import ProfilePermissionSchema
from building.auth.profile_permission.dao import ProfilePermissionDAO
from building.auth.profile_permission.model import ProfilePermissionResponse, ProfilePermissionModel


class ProfilePermissionService:
    def __init__(self, database: Session):
        self.dao = ProfilePermissionDAO(database)

    def create(self, model: ProfilePermissionModel) -> ProfilePermissionResponse:
        profile_permission = self.dao.check_profile_permission(model.profile_id, model.permission_id)
        if profile_permission:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Permission Already Defined For Permission!')
        new = ProfilePermissionSchema(
            profile_id=model.profile_id,
            permission_id=model.permission_id
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data!')

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = ProfilePermissionService(database)
#     data = ProfilePermissionModel(
#         profile_id=1,
#         permission_id=6,
#     )
#     service.create(data)
#
# finally:
#     database.close()
