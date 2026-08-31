import secrets
from utils.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date


class VisitorSchema(Base):
    __tablename__ = 'visitor'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    member_id = Column("member_id", Integer, ForeignKey("member.id"), nullable=False)
    name = Column("name", String, nullable=True)
    date = Column("date", Date, nullable=False)
    time = Column("time", String, nullable=True)
    # 'Esperando Check In','Esperdo Check Out', 'Visita Concluida', 'Convite Expirado'
    status = Column("status", String, nullable=False, default=" Waiting for Check In")
    description = Column("description", String, nullable=True)
    token = Column("token", String(64), nullable=False, unique=True, index=True,
                   default=lambda: secrets.token_urlsafe(24))
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, member_id: int, name: str, date: Date, time: str, status: str, description: str | None):
        self.member_id = member_id
        self.name = name
        self.date = date
        self.time = time
        self.status = status
        self.description = description
