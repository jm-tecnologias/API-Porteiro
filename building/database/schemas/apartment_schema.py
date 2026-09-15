from sqlalchemy.orm import relationship
from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class ApartmentSchema(Base):
    __tablename__ = 'apartment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    floor = Column("floor", String, nullable=True)
    number = Column("number", String, nullable=False)
    type = Column("type", String, nullable=True)
    description = Column("description", String, nullable=True)
    building_id = Column("building_id", Integer, ForeignKey("building.id"), nullable=False)
    occupation_state = Column("occupation_state", String, nullable=False, default='Livre')
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    building = relationship(
        "BuildingSchema",
        back_populates="apartments",
    )

    def __init__(self, floor: str, number: str, _type: str, description: str | None, occupation_state: str, building_id: int):
        self.floor = floor
        self.number = number
        self.type = _type
        self.occupation_state = occupation_state
        self.description = description
        self.building_id = building_id
