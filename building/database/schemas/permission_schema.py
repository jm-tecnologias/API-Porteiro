from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey


class PermissionSchema(Base):
    __tablename__ = "permission"
    id = Column("id", Integer, primary_key=True, index=True)
    module = Column("module", String, nullable=False)
    action = Column("action", String, nullable=False)
    code = Column("code", String, nullable=False)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
