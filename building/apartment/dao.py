from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from utils.schemas.building_schema import ApartmentSchema


class ApartmentDAO(BaseDAO[ApartmentSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=ApartmentSchema
        )

    def find_by_number(self, number: str, building_id: int) -> ApartmentSchema:
        stmt = select(self.model).where(self.model.number == number).where(self.model.building_id == building_id)
        return self.database.scalar(stmt)
