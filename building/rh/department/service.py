from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.dao import BuildingDAO
from building.database.schemas.department_schema import DepartmentSchema
from building.rh.department.dao import DepartmentDAO
from building.rh.department.model import DepartmentResponse, DepartmentModel


class DepartmentService:
    def __init__(self, database: Session):
        self.dao = DepartmentDAO(database)
        self.dao_build = BuildingDAO(database)

    def create(self, department: DepartmentModel) -> DepartmentResponse:
        building = self.dao_build.find_by_id(department.building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data Not Found!')
        new = DepartmentSchema(
            building_id=department.building_id,
            description=department.description,
            name=department.name,
            code=department.code
        )
        try:
            department = self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Data Structure Not Valid')
        return department

    def update(self, dep_id: int, department_data: DepartmentModel) -> DepartmentResponse:
        department = self.dao.find_by_id(dep_id)
        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data Not Found!')
        data = department_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(department, field, value)
        try:
            return self.dao.update(department)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Update Data')

    def find_all(self, building_id: int, skip: int, limit: int, state: bool = None) -> list[DepartmentResponse] | None:
        building = self.dao_build.find_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data Not Found!')

        departments = self.dao.list_departments(building_id=building_id, skip=skip, limit=limit)
        department_list = []
        for department in departments:
            if state is not None:
                if department.status == state:
                    department_list.append(department)
        if state is not None:
            return department_list
        return departments


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = DepartmentService(database)
#     data = DepartmentSchema(
#         code="FN-DEP-01",
#         name="Financeiro",
#         description="Departamento de contas internas",
#         building_id=1
#     )
#     dep = service.create(data)
#     print('Department Created')
#     print('ID: ', dep.id)
#     print('Code: ', dep.code)
#     print('Name: ', dep.name)
#     print('Description: ', dep.description)
#     print('Status: ', dep.status)
#     print('Created at: ', dep.created_at)
#     print('Updated at:', dep.updated_at)
# finally:
#     database.close()

# try:
#     service = DepartmentService(database)
#     data = DepartmentModel(
#         code="FIN-DEP-02",
#         description="Departamento de contas internas e externas da empresa",
#     )
#     dep = service.update(dep_id=2, department_data=data)
#     print('Department Created')
#     print('ID: ', dep.id)
#     print('Code: ', dep.code)
#     print('Name: ', dep.name)
#     print('Description: ', dep.description)
#     print('Status: ', dep.status)
#     print('Created at: ', dep.created_at)
#     print('Updated at:', dep.updated_at)
# finally:
#     database.close()
#
# try:
#     service = DepartmentService(database)
#
#     deps = service.find_all(building_id=1, skip=0, limit=100, state=False)
#     for dep in deps:
#         print('Department Created')
#         print('ID: ', dep.id)
#         print('Code: ', dep.code)
#         print('Name: ', dep.name)
#         print('Description: ', dep.description)
#         print('Status: ', dep.status)
#         print('Created at: ', dep.created_at)
#         print('Updated at:', dep.updated_at)
# finally:
#     database.close()
