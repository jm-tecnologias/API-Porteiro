from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.dao import BuildingDAO
from building.database.schemas.employee_schema import EmployeeSchema
from building.rh.employee.dao import EmployeeDAO
from building.rh.employee.model import EmployeeModel, EmployeeResponse


class EmployeeService:
    def __init__(self, database: Session):
        self.dao = EmployeeDAO(database)
        self.dao_build = BuildingDAO(database)

    def create(self, employee_data: EmployeeModel) -> EmployeeResponse:
        employee = self.dao.find_by_code(employee_data.code)
        if employee:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Employee Or Code Already Exist!')
        new = EmployeeSchema(
            building_id=employee_data.building_id,
            description=employee_data.description,
            name=employee_data.name,
            code=employee_data.code,
            surname=employee_data.surname
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                                detail='Data Structure Not Valid')

    def update(self, employee_id: int, employee_data: EmployeeModel) -> EmployeeResponse:
        employee = self.dao.find_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Employee Data Not Found!')
        data = employee_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(employee, field, value)
        try:
            return self.dao.update(employee)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Update Data!')

    def find_all(self, building_id: int, skip: int, limit: int) -> list[EmployeeResponse]:
        building = self.dao_build.find_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data Not Found!')

        employees = self.dao.list_employees(building_id=building_id, skip=skip, limit=limit)

        return employees

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = EmployeeService(database)
#     data = EmployeeModel(
#         code='S408',
#         name='Amilcar',
#         surname="Mula",
#         description='Funcionario teste',
#         building_id=1,
#     )
#     service.create(data)
#
# finally:
#     database.close()
