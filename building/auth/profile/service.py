from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.auth.profile.dao import ProfileDAO
from building.auth.profile.model import ProfileModel, ProfileResponse
from building.database.schemas.profile_schema import ProfileSchema


class ProfileService:
    def __init__(self, database: Session):
        self.dao = ProfileDAO(database)

    def create(self, profile: ProfileModel) -> ProfileResponse:
        new = ProfileSchema(
            profile=profile.profile,
            description=profile.description,
            status=profile.status
        )
        return self.dao.create(new)

    def update(self, pro_id: int, profile_data: ProfileModel) -> ProfileResponse:
        profile = self.dao.find_by_id(pro_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile Not Found!')
        data = profile_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(profile, field, value)

        try:
            return self.dao.update(profile)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Was Not Possible To Update Data!')

    def list_all(self) -> list[ProfileResponse]:
        return self.dao.find_all()


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = ProfileService(database)
#     data = ProfileModel(
#         profile="Recepcionist",
#         description="Recepcionista do Edificio",
#         status=True
#     )
#     user = service.create(data)

    # clients = service.list_all()
    # for client in clients:
    #     print(client.description)
    # service.update(4, data)
# finally:
#     database.close()
