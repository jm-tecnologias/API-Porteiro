from utils.base import Base
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date


class DepartmentEmployeeSchema(Base):
    __tablename__ = 'department_employee'
    department_id = Column("department_id", Integer, ForeignKey("department.id"), nullable=False, primary_key=True)
    employee_id = Column("employee_id", Integer, ForeignKey("employee.id"), nullable=False, primary_key=True)
    position = Column("position", String, nullable=False)
    initial_date = Column("initial_date", Date, nullable=False)
    final_date = Column("final_date", Date, nullable=True)
    description = Column("description", String, nullable=True)
    status = Column("status", Boolean, nullable=False, default=True)
    created_at = Column("created_at", DateTime, nullable=False, default=datetime.now, primary_key=True)
    updated_at = Column("updated_at", DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, department_id: int, employee_id: int, position: str, initial_date: date, final_date: date,
                 description: str | None, status: bool | True):
        self.department_id = department_id
        self.employee_id = employee_id
        self.position = position
        self.initial_date = initial_date
        self.final_date = final_date
        self.description = description
        self.status = status
