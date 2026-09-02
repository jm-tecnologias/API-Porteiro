from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from building.rh.department.model import DepartmentResponse, DepartmentModel
from building.rh.department.service import DepartmentService
from utils.database import get_database

department_router = APIRouter(prefix='/building/rh/department', tags=['Buildings', 'RH', 'Departments'])


def get_service(database: Session = Depends(get_database)) -> DepartmentService:
    return DepartmentService(database)


@department_router.get('/find-all/{building_id}/{state}', response_model=list[DepartmentResponse],
                       status_code=status.HTTP_200_OK)
async def get(building_id: int, state: bool = None,
              skip: int = Query(default=0, ge=0),
              limit: int = Query(default=100, ge=1, le=500),
              service: DepartmentService = Depends(get_service)) -> list[DepartmentResponse]:
    return service.find_all(building_id=building_id, state=state, skip=skip, limit=limit)


@department_router.post('/register', response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create(department: DepartmentModel, service: DepartmentService = Depends(get_service)) -> DepartmentResponse:
    return service.create(department)


@department_router.patch('/update/{dep_id}', response_model=DepartmentResponse,
                         status_code=status.HTTP_201_CREATED)
async def update(dep_id: int, department: DepartmentModel,
                 service: DepartmentService = Depends(get_service)) -> DepartmentResponse:
    return service.update(dep_id, department)
