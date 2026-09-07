from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.rh.department_employee.model import DepEmpResponse, DepEmpModel
from building.rh.department_employee.service import DepEmpService
from utils.database import get_database

depemp_router = APIRouter(prefix='/building/rh/employee-in-department', tags=['Buildings', 'RH', 'Employees',
                                                                              'Departments'])


def get_service(database: Session = Depends(get_database)) -> DepEmpService:
    return DepEmpService(database)


@depemp_router.get('/list-all', response_model=list[DepEmpResponse], status_code=status.HTTP_200_OK)
async def list_all(service: DepEmpService = Depends(get_service)) -> list[DepEmpResponse]:
    return service.list_all()


@depemp_router.post('/register', response_model=DepEmpResponse, status_code=status.HTTP_201_CREATED)
async def create(depemp_data: DepEmpModel, service: DepEmpService = Depends(get_service)) -> DepEmpResponse:
    return service.create(depemp_data)


@depemp_router.patch('/update', response_model=DepEmpResponse, status_code=status.HTTP_201_CREATED)
async def update(old_data: DepEmpResponse, new_data: DepEmpModel,
                 service: DepEmpService = Depends(get_service)) -> DepEmpResponse:
    return service.update(old_data, new_data)
