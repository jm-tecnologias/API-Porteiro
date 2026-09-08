from sqlalchemy.orm import relationship
from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


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
