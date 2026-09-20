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
    historical = relationship(
        "HistoricSchema",
        back_populates="client",
        order_by="HistoricSchema.created_at.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, user_id: int, surname: str, num_members: int | 1,  description: str | None, building_id: int):
        self.user_id = user_id
        self.surname = surname
        self.num_members = num_members
        self.description = description
        self.building_id = building_id



