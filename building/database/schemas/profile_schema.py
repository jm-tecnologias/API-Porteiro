from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean


class ProfileSchema(Base):
    __tablename__ = "profile"
    id = Column("id", Integer, primary_key=True, index=True)
    profile = Column("profile", String(100), nullable=False)
    description = Column("description", String(1000), nullable=True)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, profile: str, description: str | None, status: bool | True):
        self.profile = profile
        self.description = description
        self.status = status
