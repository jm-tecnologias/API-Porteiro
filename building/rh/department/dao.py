from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas.department_schema import DepartmentSchema
from utils.baseDao import BaseDAO


class DepartmentDAO(BaseDAO[DepartmentSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=DepartmentSchema
        )

    def list_departments(self, building_id: int, skip: int, limit: int) -> list[DepartmentSchema]:
        stmt = (select(DepartmentSchema).offset(skip).limit(limit)
                .order_by(DepartmentSchema.name).where(DepartmentSchema.building_id == building_id))
        return list(self.database.scalars(stmt).all())
