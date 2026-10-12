from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from building.check_in_out.visitor.dao import VisitorCheckInOutDAO
from building.check_in_out.visitor.model import VisitorCheckInOutResponse, VisitorCheckInOutModel
from building.database.schemas import VisitorCheckInOutSchema


class VisitorCheckInOutService:
    def __init__(self, database: Session):
        self.dao = VisitorCheckInOutDAO(database)

    def create(self, model: VisitorCheckInOutModel) -> VisitorCheckInOutResponse:
        new = VisitorCheckInOutSchema(
            visitor_id=model.visitor_id,
            user_id=model.user_id,
            status=model.status,
            note=model.note
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Was Not Possible To Add Data!')
