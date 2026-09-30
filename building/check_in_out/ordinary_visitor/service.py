from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.database.schemas import OrdinaryVisitorSchema
from building.occupational_historic.check_in_out.ordinary_visitor.dao import OrdinaryVisitorDAO
from building.occupational_historic.check_in_out.ordinary_visitor.model import OrdinaryVisitorResponse, \
    OrdinaryVisitorModel


class OrdinaryVisitorService:
    def __init__(self, database: Session):
        self.dao = OrdinaryVisitorDAO(database)

    def create(self, model: OrdinaryVisitorModel) -> OrdinaryVisitorResponse:
        new = OrdinaryVisitorSchema(
            member_id=model.member_id,
            user_id=model.user_id,
            name=model.name,
            phone=model.phone,
            status=model.status,
            description=model.description
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data')

    def list_all(self) -> list[OrdinaryVisitorResponse]:
        return self.dao.find_all()


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = OrdinaryVisitorService(database)
#     data = OrdinaryVisitorModel(
#         member_id=1,
#         user_id=1,
#         name="Visitante de teste",
#         phone='878201993',
#         status='Check In',
#         description='Visitante aguarda na recepcao'
#     )
#     service.create(data)
# finally:
#     database.close()