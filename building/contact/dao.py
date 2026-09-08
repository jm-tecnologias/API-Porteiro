from sqlalchemy import select
from sqlalchemy.orm import Session

from building.contact.model import ContactResponse
from utils.baseDao import BaseDAO
from building.database.schemas.building_schema import ContactSchema


class ContactDAO(BaseDAO[ContactSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=ContactSchema
        )

    def list_contacts(self, building_id: int, skip: int = 0, limit: int = 100) -> list[ContactResponse]:
        stmt = (select(ContactSchema).offset(skip).limit(limit)
                .order_by(ContactSchema.id)
                .where(ContactSchema.building_id == building_id))
        return list(self.database.scalars(stmt).all())
