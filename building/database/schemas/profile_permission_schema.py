from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey


class ProfilePermissionSchema(Base):
    __tablename__ = "profile_permission"
    profile_id = Column("profile_id", Integer, ForeignKey("profile.id"), nullable=False, primary_key=True,)
    permission_id = Column("permission_id", Integer, ForeignKey("permission.id"), nullable=False, primary_key=True,)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
