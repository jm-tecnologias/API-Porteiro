from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from utils.schemas.building_schema import EmployeeSchema


class EmployeeDAO(BaseDAO[EmployeeSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EmployeeSchema
        )

    def list_employees(self, building_id: int, skip: int, limit: int) -> list[EmployeeSchema]:
        stmt = (select(EmployeeSchema).offset(skip).limit(limit)
                .order_by(EmployeeSchema.id).where(EmployeeSchema.building_id == building_id))
        return list(self.database.scalars(stmt).all())
