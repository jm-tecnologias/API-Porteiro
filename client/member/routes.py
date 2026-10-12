from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from client.member.MemberDashboardResponse import DashboardResponse
from client.member.model import MemberModel, MemberResponse
from client.member.service import MemberService
from utils.database import get_database

member_router = APIRouter(prefix='/client/member', tags=['Buildings', 'Clients', 'Members'])


def get_service(database: Session = Depends(get_database)) -> MemberService:
    return MemberService(database)


# @member_router.patch('/update/{member_id}', response_model=MemberResponse, status_code=status.HTTP_200_OK)
# async def update(member_id: int, model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
#     return service.update(member_id, model)


@member_router.get('/dashboard/get/{token}', response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def get_dashboard_data(token: str, req: Request,
                             service: MemberService = Depends(get_service)) -> DashboardResponse:
    return service.populate_dashboard(token, str(req.base_url))


@member_router.patch('/update/profile/{token}', response_model=MemberResponse, status_code=status.HTTP_200_OK)
async def update(token: str, model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.update_by_logged_client(token, model)
