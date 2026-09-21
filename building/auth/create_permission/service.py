from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from building.database.schemas import PermissionSchema
from building.auth.create_permission.dao import PermissionDAO
from building.auth.create_permission.model import PermissionResponse, PermissionModel


class PermissionService:
    def __init__(self, database: Session):
        self.dao = PermissionDAO(database)

    def create(self, model: PermissionModel) -> PermissionResponse:
        permission = self.dao.check_permission(model.module, model.action)
        if permission:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Permission already Exist!')
        new = PermissionSchema(
            module=model.module,
            action=model.action,
            code=str(model.module+":"+model.action)
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data!')

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = PermissionService(database)
#     data = PermissionModel(
#         module="USER",
#         action="DELETE",
#     )
#     user = service.create(data)
#
# finally:
#     database.close()