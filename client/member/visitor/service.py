from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from building.barcode_service import BarcodeService
from client.member.visitor.dao import VisitorDAO
from client.member.visitor.model import VisitorResponse, VisitorModel
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
                BarcodeService.generate_barcode('V', new_visitor.token)
            return new_visitor

        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Was Not Possible To Add Data!')
