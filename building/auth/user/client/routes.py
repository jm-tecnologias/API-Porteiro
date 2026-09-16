from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.user.client.model import LoginResponse, UserMemberModel
from building.auth.user.client.service import UserMemberService
from utils.database import get_database

client_user_router = APIRouter(prefix='/auth/client', tags=['Authentication', 'login'])


def get_service(database: Session = Depends(get_database)) -> UserMemberService:
    return UserMemberService(database)


@client_user_router.post('/login', response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(model: UserMemberModel, service: UserMemberService = Depends(get_service)) -> LoginResponse:
    return service.get_user_login(model.username, model.password)
