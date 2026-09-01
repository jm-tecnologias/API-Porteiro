from sqlalchemy.orm import relationship
from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class BuildingSchema(Base):
    __tablename__ = "building"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)
    status = Column("status", Boolean, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    contacts = relationship(
        "ContactSchema",
        back_populates="building",
        order_by="ContactSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    departments = relationship(
        "DepartmentSchema",
        back_populates="building",
        order_by="DepartmentSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    employees = relationship(
        "EmployeeSchema",
        back_populates="building",
        order_by="EmployeeSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    apartments = relationship(
        "ApartmentSchema",
        back_populates="building",
        order_by="ApartmentSchema.id.asc()",
        cascade="all, delete-orphan",
    )
    clients = relationship(
        "ClientSchema",
        back_populates="building",
        order_by="ClientSchema.id.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, name: str, description: str | None):
        self.name = name
        self.description = description


class ContactSchema(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column("phone", String, nullable=False, unique=True)
    email = Column("email", String, nullable=True)
    website = Column("website", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="contacts",
    )

    def __init__(self, phone: str, email: str | None, website: str | None, building_id: int):
        self.phone = phone
        self.email = email
        self.website = website
        self.building_id = building_id


class AddressSchema(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    province = Column("province", String, nullable=False)
    city = Column("city", String, nullable=False)
    nearby_hood = Column("nearby_hood", String, nullable=True)
    avenue = Column("avenue", String, nullable=True)
    number = Column("number", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, province: str, city: str, nearby_hood: str | None, avenue: str | None, number: int | None):
        self.province = province
        self.city = city
        self.nearby_hood = nearby_hood
        self.avenue = avenue
        self.number = number


class DepartmentSchema(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column("code", String, nullable=False, unique=True)
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="departments",
    )

    def __init__(self, code: str, name: str, description: str | None, building_id: int):
        self.code = code
        self.name = name
        self.description = description
        self.building_id = building_id


class EmployeeSchema(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column("code", String, nullable=False, unique=True)
    name = Column("name", String, nullable=False)
    surname = Column("surname", String, nullable=False)
    description = Column("description", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="employees",
    )

    def __init__(self, code: str, name: str, surname: str, description: str | None, building_id: int):
        self.code = code
        self.name = name
        self.surname = surname
        self.description = description
        self.building_id = building_id


class ApartmentSchema(Base):
    __tablename__ = 'apartment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    floor = Column("floor", String, nullable=True)
    number = Column("number", String, nullable=False)
    type = Column("type", String, nullable=True)
    description = Column("description", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="apartments",
    )

    def __init__(self, floor: str, number: str, _type: str, description: str | None, building_id: int):
        self.floor = floor
        self.number = number
        self.type = _type
        self.description = description
        self.building_id = building_id


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
        order_by="ClientSchema.created_at.asc()",
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
