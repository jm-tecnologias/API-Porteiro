from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas.employee_user_schema import EmployeeUserSchema
from utils.baseDao import BaseDAO


class UserDAO(BaseDAO[EmployeeUserSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=EmployeeUserSchema
        )

    def find_by_username(self, username: str) -> EmployeeUserSchema:
        stmt = select(EmployeeUserSchema).where(EmployeeUserSchema.username == username)
        return self.database.scalar(stmt)
