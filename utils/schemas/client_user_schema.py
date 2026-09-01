from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class MemberUserSchema(Base):
    __tablename__ = 'member_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    description = Column("description", String, nullable=True)
    member_id = Column("member_id", Integer, ForeignKey("member.id"), nullable=False)
    profile_id = Column("profile_id", Integer, ForeignKey("profile.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, username: str, password: str, description: str | None, member_id: int,
                 profile_id: int, status: bool | True):
        self.username = username
        self.password = password
        self.description = description
        self.member_id = member_id
        self.profile_id = profile_id
        self.status = status
