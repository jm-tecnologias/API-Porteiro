from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.user.employee.model import UserResponse, UserModel
from building.auth.user.employee.service import UserService
from utils.database import get_database

employee_user_router = APIRouter(prefix='/auth/employee', tags=['Authentication', 'Login'])


def get_service(database: Session = Depends(get_database)) -> UserService:
    return UserService(database)


@employee_user_router.post('/login', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login(model: UserModel, service: UserService = Depends(get_service)) -> UserResponse:
    return service.get_user_login(model.username, model.password)
