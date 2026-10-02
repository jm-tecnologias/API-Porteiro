from sqlalchemy import select
from sqlalchemy.orm import Session
from building.database.schemas.member_user_schema import UserMemberSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")


class UserMemberDAO(BaseDAO[UserMemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=UserMemberSchema
        )

    def find_by_username(self, username: str) -> UserMemberSchema:
        stmt = select(UserMemberSchema).where(UserMemberSchema.username == username)
        return self.database.scalar(stmt)


