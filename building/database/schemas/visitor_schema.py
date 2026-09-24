import secrets

from sqlalchemy.orm import relationship

from building.database.base import Base
from datetime import datetime, date, time
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time


class VisitorSchema(Base):
    __tablename__ = 'visitor'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    member_id = Column("member_id", Integer, ForeignKey("member.id"), nullable=False)
    name = Column("name", String, nullable=True)
    phone = Column("phone", String, nullable=True)
    visitor_date = Column("visitor_date", Date, nullable=False)
    visitor_time = Column("visitor_time", Time, nullable=True)
    # 'Esperando Check In','Esperando Check Out', 'Visita Concluida', 'Convite Expirado', 'Convite Cancelado'
    status = Column("status", String, nullable=False, default="Esperando Check In")
    description = Column("description", String, nullable=True)
    token = Column("token", String(64), nullable=False, unique=True, index=True,
                   default=lambda: secrets.token_urlsafe(24))
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    member = relationship(
        "MemberSchema",
        back_populates="visitors",
    )
    visitor_check_historic = relationship(
        "VisitorCheckInOutSchema",
        back_populates="visitor",
        order_by="VisitorCheckInOutSchema.created_at.asc()",
        cascade="all, delete-orphan",
    )

    def __init__(self, member_id: int, name: str, phone: str,
                 visitor_date: date, visitor_time: time, description: str | None):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.visitor_date = visitor_date
        self.visitor_time = visitor_time
        self.description = description
