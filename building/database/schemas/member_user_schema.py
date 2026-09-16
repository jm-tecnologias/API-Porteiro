from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class UserMemberSchema(Base):
    __tablename__ = 'member_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    description = Column("description", String, nullable=True)
    member_id = Column("member_id", Integer, ForeignKey("member.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, username: str, password: str, description: str | None, member_id: int,
                 status: bool | True):
        self.username = username
        self.password = password
        self.description = description
        self.member_id = member_id
        self.status = status


# class UserHistorySchema(Base):
#     __tablename__ = "user_history"
#
#     id = Column("id", Integer, primary_key=True, autoincrement=True)
#     user_id = Column("user_id", Integer, ForeignKey("user.id"), nullable=False)
#     action = Column("action", String, nullable=False)
#     accessed_at = Column("accessed_at", DateTime, default=datetime.now, nullable=False)
#     user = relationship(
#         "UserSchema",
#         back_populates="histories",
#     )
#
#     def __init__(self, user_id, action):
#         self.user_id = user_id
#         self.action = action
