from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from building.rh.employee.model import EmployeeResponse, EmployeeModel
from building.rh.employee.service import EmployeeService
from utils.database import get_database

employee_router = APIRouter(prefix='/building/rh/employee', tags=['Buildings', 'RH', 'Employees'])


def get_service(database: Session = Depends(get_database)) -> EmployeeService:
    return EmployeeService(database)


@employee_router.get('/find-all/{building_id}', response_model=list[EmployeeResponse],
                     status_code=status.HTTP_200_OK)
async def get(building_id: int, skip: int = Query(default=0, ge=0),
              limit: int = Query(default=100, ge=1, le=500),
              service: EmployeeService = Depends(get_service)) -> list[EmployeeResponse]:
    return service.find_all(building_id, skip, limit)


@employee_router.post('/register', response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create(employee: EmployeeModel, service: EmployeeService = Depends(get_service)) -> EmployeeResponse:
    return service.create(employee)


@employee_router.patch('/update/{employee_id}', response_model=EmployeeResponse,
                       status_code=status.HTTP_201_CREATED)
async def update(employee_id: int, employee: EmployeeModel,
                 service: EmployeeService = Depends(get_service)) -> EmployeeResponse:
    return service.update(employee_id, employee)
