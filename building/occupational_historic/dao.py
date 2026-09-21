from sqlalchemy import select
from sqlalchemy.orm import Session
from building.database.schemas import HistoricSchema, ApartmentSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")


class HistoricDAO(BaseDAO[HistoricSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=HistoricSchema
        )

    def list_all(self) -> T:
        stmt = (select(HistoricSchema, ApartmentSchema)
                .join(ApartmentSchema, HistoricSchema.apartment_id == ApartmentSchema.id)
                )
        return self.database.execute(stmt).all()

    def find_by_created_at(self, created_at: str) -> HistoricSchema:
        stmt = select(HistoricSchema).where(HistoricSchema.created_at.like(f'{created_at}%'))
        return self.database.scalar(stmt)
