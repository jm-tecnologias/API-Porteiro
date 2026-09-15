# from sqlalchemy import select
# from sqlalchemy.orm import Session
#
# from building.database.schemas.member_user_schema import MemberUserSchema
# from utils.baseDao import BaseDAO
#
#
# class UserMemberDAO(BaseDAO[MemberUserSchema]):
#     def __init__(self, database: Session):
#         super().__init__(
#             database=database,
#             model=MemberUserSchema
#         )
#
#     def find_by_username(self, username: str) -> MemberUserSchema:
#         stmt = select(MemberUserSchema).where(MemberUserSchema.username == username)
#         return self.database.scalar(stmt)
