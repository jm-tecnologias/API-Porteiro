from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas.employee_user_schema import UserEmployeeSchema
from utils.baseDao import BaseDAO


class UserEmployeeDAO(BaseDAO[UserEmployeeSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=UserEmployeeSchema
        )

    def find_by_username(self, username: str) -> UserEmployeeSchema:
        stmt = select(UserEmployeeSchema).where(UserEmployeeSchema.username == username)
        return self.database.scalar(stmt)
