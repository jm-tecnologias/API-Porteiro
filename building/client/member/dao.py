from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import MemberSchema, ApartmentSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")


class MemberDAO(BaseDAO[MemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=MemberSchema
        )

    def find_member(self, token: str) -> T:
        stmt = (
            select(MemberSchema, ApartmentSchema)
            .join(ApartmentSchema, MemberSchema.apartment_id == ApartmentSchema.id)
            .where(MemberSchema.token == token))
        return self.database.execute(stmt).one_or_none()
