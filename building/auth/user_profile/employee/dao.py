from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import UserProfileEmployeeSchema
from utils.baseDao import BaseDAO


class UserProfileDAO(BaseDAO[UserProfileEmployeeSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=UserProfileEmployeeSchema
        )

    def check_user_profile(self, profile_id: int, employee_user_id: int) -> UserProfileEmployeeSchema:
        stmt = (select(UserProfileEmployeeSchema).where(UserProfileEmployeeSchema.profile_id == profile_id)
                .where(UserProfileEmployeeSchema.employee_user_id == employee_user_id)
                .where(UserProfileEmployeeSchema.status == 1))
        return self.database.scalar(stmt)
