from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.user.client.model import LoginResponse, UserMemberModel, TokenResponse, DashboardResponse
from building.auth.user.client.service import UserMemberService
from utils.database import get_database

client_user_router = APIRouter(prefix='/building/auth/user/client', tags=['Authentication', 'login'])


def get_service(database: Session = Depends(get_database)) -> UserMemberService:
    return UserMemberService(database)


@client_user_router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: UserMemberModel, service: UserMemberService = Depends(get_service)) -> TokenResponse:
    return service.get_user_login(credentials.username, credentials.password)


@client_user_router.get('/dashboard/get/{token}', response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def get_dashboard_data(token: str, service: UserMemberService = Depends(get_service)) -> DashboardResponse:
    return service.populate_dashboard(token)

