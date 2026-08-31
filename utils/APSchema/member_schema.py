from sqlalchemy.orm import relationship
from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class MemberSchema(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False)
    client_id = Column("client_id", Integer, ForeignKey("client.id"), nullable=False)
    doc_id = Column("doc_id", String, nullable=False)
    name = Column("name", String, nullable=True)
    surname = Column("surname", String, nullable=False)
    phone = Column("phone", String, nullable=True)
    email = Column("email", String, nullable=True)
    description = Column("description", String, nullable=True)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    client = relationship(
        "ClientSchema",
        back_populates="members",
    )
    checkedStatus = relationship(
        "CheckInOutSchema",
        back_populates="member",
        order_by="ClientSchema.created_at.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, user_id: int, client_id: int, doc_id: str, name: str,  surname: str, phone: str | None,
                 email: str | None, description: str | None, status: bool | True):
        self.user_id = user_id
        self.client_id = client_id
        self.doc_id = doc_id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.description = description
        self.status = status
