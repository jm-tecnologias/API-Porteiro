from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from building.barcode_service import BarcodeService
from building.client.member.visitor.dao import VisitorDAO
from building.client.member.visitor.model import VisitorResponse, VisitorModel
from building.database.schemas import VisitorSchema


class VisitorService:
    def __init__(self, database: Session):
        self.dao = VisitorDAO(database)

    def create(self, visitor_model: VisitorModel) -> VisitorResponse:
        new = VisitorSchema(
            member_id=visitor_model.member_id,
            name=visitor_model.name,
            phone=visitor_model.phone,
            visitor_date=visitor_model.visitor_date,
            visitor_time=visitor_model.visitor_time,
            description=visitor_model.description,
        )

        try:
            new_visitor = self.dao.create(new)
            if new_visitor:
                BarcodeService.generate_barcode('V', new_visitor.id)
            return new_visitor

        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible TO Add Data!')

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = VisitorService(database)
#     model = VisitorModel(
#         member_id=1,
#         name='sdfgd Mula Jr.',
#         phone='847100793',
#         visitor_date='2026-09-24',
#         visitor_time='16:00',
#         description='Visita de uma Semana'
#     )
#     model = service.create(model)
#     print(model)
# finally:
#    database.close()
