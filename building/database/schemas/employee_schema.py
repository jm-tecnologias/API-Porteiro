from sqlalchemy.orm import relationship
from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class EmployeeSchema(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column("code", String(10), nullable=False, unique=True)
    name = Column("name", String(30), nullable=False)
    surname = Column("surname", String(50), nullable=False)
    description = Column("description", String(1000), nullable=True)
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
