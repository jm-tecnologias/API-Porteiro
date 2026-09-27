from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey


class UserProfileEmployeeSchema(Base):
    __tablename__ = "user_profile_employee"
    profile_id = Column("profile_id", Integer, ForeignKey("profile.id"), nullable=False, primary_key=True,)
    employee_user_id = Column("employee_user_id", Integer, ForeignKey("employee_user.id"), nullable=False, primary_key=True,)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, profile_id: int, employee_user_id: int):
        self.profile_id = profile_id
        self.employee_user_id = employee_user_id
