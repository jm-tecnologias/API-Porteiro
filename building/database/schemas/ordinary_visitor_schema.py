from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date


class OrdinaryVisitorSchema(Base):
    __tablename__ = 'ordinary_visitor'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    member_id = Column("member_id", Integer, ForeignKey("client.id"), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False)
    name = Column("name", String, nullable=True)
    phone = Column("phone", String, nullable=True)
    # 'Check In','Check Out'
    status = Column("status", String, nullable=False, default="Check In")
    description = Column("description", String, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, member_id: int, user_id: int, name: str, phone: str | None, status: str, description: str | None):
        self.member_id = member_id
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.status = status
        self.description = description
