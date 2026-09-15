from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import UserProfileMemberSchema
from utils.baseDao import BaseDAO


class UserProfileMemberDAO(BaseDAO[UserProfileMemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=UserProfileMemberSchema
        )

    def check_user_profile(self, profile_id: int, member_user_id: int) -> UserProfileMemberSchema:
        stmt = (select(UserProfileMemberSchema).where(UserProfileMemberSchema.profile_id == profile_id)
                .where(UserProfileMemberSchema.member_user_id == member_user_id)
                .where(UserProfileMemberSchema.status == 1))
        return self.database.scalar(stmt)
