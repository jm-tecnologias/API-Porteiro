from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey


class UserProfileMemberSchema(Base):
    __tablename__ = "user_profile_member"
    profile_id = Column("profile_id", Integer, ForeignKey("create_profile.id"), nullable=False, primary_key=True,)
    member_user_id = Column("member_user_id", Integer, ForeignKey("member_user.id"), nullable=False, primary_key=True,)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, profile_id: int, member_user_id: int):
        self.profile_id = profile_id
        self.member_user_id = member_user_id
