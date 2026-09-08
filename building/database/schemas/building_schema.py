from sqlalchemy.orm import relationship
from building.database.base import Base
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

    def __init__(self, building_id: int, province: str, city: str, nearby_hood: str | None, avenue: str | None,
                 number: int | None):
        self.building_id = building_id
        self.province = province
        self.city = city
        self.nearby_hood = nearby_hood
        self.avenue = avenue
        self.number = number

