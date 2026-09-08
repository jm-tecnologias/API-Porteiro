from sqlalchemy.orm import relationship
from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class ClientSchema(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False)
    surname = Column("surname", String, nullable=True)
    num_members = Column("num_members", Integer, nullable=False, default=1)
    description = Column("description", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="clients",
    )
    members = relationship(
        "MemberSchema",
        back_populates="client",
        order_by="MemberSchema.id.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, user_id: int, surname: str, num_members: int | 1,  description: str | None, building_id: int):
        self.user_id = user_id
        self.surname = surname
        self.num_members = num_members
        self.description = description
        self.building_id = building_id


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
        order_by="CheckInOutSchema.created_at.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, user_id: int, client_id: int, doc_id: str, name: str,  surname: str, phone: str | None,
                 email: str | None, description: str | None):
        self.user_id = user_id
        self.client_id = client_id
        self.doc_id = doc_id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.description = description


class CheckInOutSchema(Base):
    __tablename__ = 'check_in_out'
    member_id = Column("member_id", Integer, ForeignKey("member.id"), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False, primary_key=True)
    status = Column("status", String, nullable=False)  # ENUM('Check In', 'Check Out')
    note = Column("note", String, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now, primary_key=True)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    member = relationship(
        "MemberSchema",
        back_populates="checkedStatus",
    )

    def __init__(self, member_id: int, user_id: int, status: str, note: str | None):
        self.member_id = member_id
        self.user_id = user_id
        self.status = status
        self.note = note
