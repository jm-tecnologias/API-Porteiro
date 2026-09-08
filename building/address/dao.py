from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from building.database.schemas.building_schema import AddressSchema


class AddressDAO(BaseDAO[AddressSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=AddressSchema
        )

    def find_address(self, building_id: int) -> AddressSchema:
        stmt = select(AddressSchema).where(AddressSchema.building_id == building_id)
        return self.database.scalar(stmt)

    def find_by_number(self, number: int) -> AddressSchema:
        stmt = select(AddressSchema).where(AddressSchema.number == number)
        return self.database.scalar(stmt)
