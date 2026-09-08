from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from building.database.schemas.depart_employee_schema import DepartmentEmployeeSchema


class DepEmpDAO(BaseDAO[DepartmentEmployeeSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=DepartmentEmployeeSchema
        )

    def get_dep_emp(self, department_id: int, employee_id: int, created_at: datetime) -> DepartmentEmployeeSchema:
        stmt = (select(DepartmentEmployeeSchema)
                .where(DepartmentEmployeeSchema.department_id == department_id)
                .where(DepartmentEmployeeSchema.employee_id == employee_id)
                .where(DepartmentEmployeeSchema.created_at == created_at))
        return self.database.scalar(stmt)

    def list_department_employees(self, employee_id: int) -> list[DepartmentEmployeeSchema]:
        stmt = select(DepartmentEmployeeSchema).where(DepartmentEmployeeSchema.employee_id == employee_id)
        return list(self.database.scalars(stmt).all())


