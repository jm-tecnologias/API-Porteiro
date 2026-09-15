from sqlalchemy.orm import relationship

from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class VisitorCheckInOutSchema(Base):
    __tablename__ = 'visitor_check_in_out'
    visitor_id = Column("visitor_id", Integer, ForeignKey("visitor.id"), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False, primary_key=True)
    # ENUM('Check In', 'Check Out', 'Saida Solicitada')
    status = Column("status", String, nullable=False, default="Check In")
    note = Column("note", String, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now, primary_key=True)
    visitor = relationship(
        "VisitorSchema",
        back_populates="visitor_check_historic",
    )

    def __init__(self, visitor_id: int, user_id: int, status: str, note: str | None):
        self.visitor_id = visitor_id
        self.user_id = user_id
        self.status = status
        self.note = note
