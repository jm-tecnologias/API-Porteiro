from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from building.rh.department.dao import DepartmentDAO
from building.rh.department_employee.dao import DepEmpDAO
from building.rh.department_employee.model import DepEmpResponse, DepEmpModel
from building.rh.employee.dao import EmployeeDAO
from building.database.schemas.depart_employee_schema import DepartmentEmployeeSchema

# Falta apenas definir as rotas


class DepEmpService:
    def __init__(self, database: Session):
        self.dao = DepEmpDAO(database)
        self.dao_dep = DepartmentDAO(database)
        self.dao_emp = EmployeeDAO(database)

    def create(self, depemp: DepEmpModel) -> DepEmpResponse:
        # verificar se o novo registo tem estado activo
        if depemp.status:
            # se o estado for activo, verificar se existe algum registo desse employee
            employee_departments = self.dao.list_department_employees(depemp.employee_id)
            if employee_departments is not None:
                # se encontrar, verificar se tal estado esta activo
                for employee_department in employee_departments:
                    # se activo:
                    if employee_department.status:
                        # desactivar
                        # registar data final como a data de desactivacao
                        self.employee_create_helper(employee_department)

        new = DepartmentEmployeeSchema(
            department_id=depemp.department_id,
            description=depemp.description,
            status=depemp.status,
            employee_id=depemp.employee_id,
            position=depemp.position,
            final_date=depemp.final_date,
            initial_date=depemp.initial_date
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Data Structure Not Valid')

    def employee_create_helper(self, depemp: DepEmpResponse):
        dep_emp = self.dao.get_dep_emp(depemp.department_id, depemp.employee_id, depemp.created_at)
        data_to_update = DepEmpModel(
            final_date=date.today(),
            status=False
        )
        data = data_to_update.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(dep_emp, field, value)
        try:
            self.dao.update(dep_emp)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Data Structure Not Valid!')

    def list_all(self) -> list[DepEmpResponse]:
        return self.dao.find_all()

    def update(self, old_data: DepEmpResponse, new_data: DepEmpModel) -> DepEmpResponse:
        dep_emp = self.dao.get_dep_emp(old_data.department_id, old_data.employee_id, old_data.created_at)
        if not dep_emp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data Not Found!')

        data = new_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(dep_emp, field, value)
        try:
            return self.dao.update(dep_emp)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was not Possible To Update Data!')



# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = DepEmpService(database)
#     model = DepEmpModel(
#         department_id=1,
#         employee_id=1,
#         status=True,
#         position="Director Teste 1",
#         initial_date=date.today(),
#         description="Promocao do employee 1 de cargo de Gestor para Director Teste 1"
#     )
#     res = service.create(model)
#     print("Cadastrado Employee ao departamento")
#     print("Dep ID: ", res.department_id)
#     print("Emp ID: ", res.employee_id)
#     print("Status: ", res.status)
#     print("Position: ", res.position)
#     print("Initial Date: ", res.initial_date)
#     print("Final Date: ", res.final_date)
#     print("Description: ", res.description)
#     print("Created at: ", res.created_at)
#     print("Updated at: ", res.updated_at)
#     print("")
#
# finally:
#     database.close()

# try:
#     service = DepEmpService(database)
#
#     list_res = service.list_all()
#     for res in list_res:
#         print("Cadastrado Employee ao departamento")
#         print("Dep ID: ", res.department_id)
#         print("Emp ID: ", res.employee_id)
#         print("Status: ", res.status)
#         print("Position: ", res.position)
#         print("Initial Date: ", res.initial_date)
#         print("Final Date: ", res.final_date)
#         print("Description: ", res.description)
#         print("Created at: ", res.created_at)
#         print("Updated at: ", res.updated_at)
#         print("____________________________________________________")
#
# finally:
#     database.close()

# try:
#     service = DepEmpService(database)
#     old_model = DepEmpResponse(
#         department_id=1,
#         employee_id=1,
#         status=True,
#         position="Director Teste 4",
#         initial_date="2026-09-03",
#         final_date=None,
#         description="Promocao do employee 1 de cargo de Gestor para Director Teste 4",
#         created_at="2026-09-03 21:46:01.972676",
#         updated_at="2026-09-03 21:46:01.972679"
#     )
#     new_model = DepEmpModel(
#         status=False,
#         final_date="2026-09-04",
#     )
#     res = service.update(old_model, new_model)
#     print("Cadastrado Employee ao departamento")
#     print("Dep ID: ", res.department_id)
#     print("Emp ID: ", res.employee_id)
#     print("Status: ", res.status)
#     print("Position: ", res.position)
#     print("Initial Date: ", res.initial_date)
#     print("Final Date: ", res.final_date)
#     print("Description: ", res.description)
#     print("Created at: ", res.created_at)
#     print("Updated at: ", res.updated_at)
#     print("")
#
# finally:
#     database.close()


