from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.database.schemas import HistoricSchema
from building.occupational_historic.dao import HistoricDAO
from building.occupational_historic.model import HistoricResponse, HistoricModel


class HistoricService:
    def __init__(self, database: Session):
        self.dao = HistoricDAO(database)

    def create(self, model: HistoricModel) -> HistoricResponse:
        new = HistoricSchema(
            client_id=model.client_id,
            user_id=model.user_id,
            apartment_id=model.apartment_id,
            occupational_date=model.occupational_date,
            final_date=model.final_date,
            description=model.description,
            num_members=model.num_members
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data!')

    def list_all(self) -> list[HistoricResponse]:
        return self.dao.find_all()


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = HistoricService(database)
#     data = HistoricModel(
#         client_id=1,
#         user_id=1,
#         apartment_id=1,
#         occupational_date='2026-08-31',
#         # final_date=model.final_date,
#         description='Test',
#         num_members=4
#     )
#     service.create(data)
# finally:
#     database.close()
