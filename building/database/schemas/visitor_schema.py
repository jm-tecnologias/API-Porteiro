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
    date = Column("date", Date, nullable=False)
    time = Column("time", Time, nullable=True)
    # 'Esperando Check In','Esperdo Check Out', 'Visita Concluida', 'Convite Expirado'
    status = Column("status", String, nullable=False, default=" Waiting for Check In")
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

    def __init__(self, member_id: int, name: str, __date: date, __time: time, status: str, description: str | None):
        self.member_id = member_id
        self.name = name
        self.date = __date
        self.time = __time
        self.status = status
        self.description = description
