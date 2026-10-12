import secrets
from sqlalchemy.orm import relationship
from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class MemberSchema(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False)
    client_id = Column("client_id", Integer, ForeignKey("client.id"), nullable=False)
    apartment_id = Column("apartment_id", Integer, ForeignKey("apartment.id"), nullable=False)
    doc_id = Column("doc_id", String(25), nullable=False)
    name = Column("name", String(50), nullable=True)
    surname = Column("surname", String(50), nullable=False)
    phone = Column("phone", String(30), nullable=True)
    email = Column("email", String(50), nullable=True)
    client_relationship = Column("client_relationship", String(50), nullable=True)
    # Adicionar url de foto de perfil
    profile_pic_url = Column("profile_pic_url", String(1000), nullable=True)
    description = Column("description", String(1000), nullable=True)
    status = Column("status", Boolean, nullable=False, default=True)
    token = Column("token", String(64), nullable=False, unique=True, index=True,
                   default=lambda: secrets.token_urlsafe(24))
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    client = relationship(
        "ClientSchema",
        back_populates="members",
    )
    checkedStatus = relationship(
        "MemberCheckInOutSchema",
        back_populates="member",
        order_by="MemberCheckInOutSchema.created_at.desc()",
        cascade="all, delete-orphan",
    )
    visitors = relationship(
        "VisitorSchema",
        back_populates="member",
        order_by="VisitorSchema.created_at.desc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, user_id: int, client_id: int, apartment_id: int, doc_id: str, name: str,  surname: str,
                 phone: str | None, email: str | None, client_relationship: str | None, description: str | None,
                 profile_pic_url: str | None):
        self.user_id = user_id
        self.client_id = client_id
        self.apartment_id = apartment_id
        self.doc_id = doc_id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.client_relationship = client_relationship
        self.description = description
        self.profile_pic_url = profile_pic_url
