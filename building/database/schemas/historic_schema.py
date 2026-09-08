from building.database.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date


class HistoricSchema(Base):
    __tablename__ = 'historic'
    client_id = Column("client_id", Integer, ForeignKey("client.id"), nullable=False, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("employee_user.id"), nullable=False, primary_key=True)
    apartment_id = Column("apartment_id", Integer, ForeignKey("apartment.id"), nullable=False, primary_key=True)
    occupational_date = Column("occupational_date", Date, nullable=False)
    final_date = Column("final_date", Date, nullable=True)
    description = Column("description", String, nullable=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now, primary_key=True)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, client_id: int, user_id: int, apartment_id: int, occupational_date: Date, final_date: Date,
                 description: str | None):
        self.client_id = client_id
        self.user_id = user_id
        self.apartment_id = apartment_id
        self.occupational_date = occupational_date
        self.final_date = final_date
        self.description = description
