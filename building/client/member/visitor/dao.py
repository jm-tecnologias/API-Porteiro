from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import VisitorSchema, MemberSchema, ApartmentSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")


class VisitorDAO(BaseDAO[VisitorSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=VisitorSchema
        )

    def find_visitor(self, visitor_id: int) -> T:
        stmt = (
            select(VisitorSchema, MemberSchema, ApartmentSchema)
            .join(MemberSchema, MemberSchema.id == VisitorSchema.member_id)
            .join(ApartmentSchema, MemberSchema.apartment_id == ApartmentSchema.id)
            .where(VisitorSchema.id == visitor_id))
        return self.database.execute(stmt).one_or_none()
