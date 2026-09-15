from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.create_user.employee.model import UserEmployeeResponse, UserEmployeeModel
from building.auth.create_user.employee.service import UserEmployeeService
from utils.database import get_database

employee_user_router = APIRouter(prefix='/auth/employee', tags=['Authentication', 'Login'])


def get_service(database: Session = Depends(get_database)) -> UserEmployeeService:
    return UserEmployeeService(database)


@employee_user_router.post('/login', response_model=UserEmployeeResponse, status_code=status.HTTP_200_OK)
async def login(model: UserEmployeeModel, service: UserEmployeeService = Depends(get_service)) -> UserEmployeeResponse:
    return service.get_user_login(model.username, model.password)
