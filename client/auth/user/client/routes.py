from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from client.auth.user.client.model import TokenResponse, UserMemberModel
from client.auth.user.client.service import UserMemberService
from utils.database import get_database

user_router = APIRouter(prefix='/client/auth/user', tags=['Authentication', 'login'])


def get_service(database: Session = Depends(get_database)) -> UserMemberService:
    return UserMemberService(database)


@user_router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: UserMemberModel, service: UserMemberService = Depends(get_service)) -> TokenResponse:
    return service.get_user_login(credentials.username, credentials.password)
