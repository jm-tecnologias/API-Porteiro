from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from building.client.member.MemberDashboardResponse import DashboardResponse
from building.client.member.MemberApartmentResponse import MemberApartmentResponse
from building.client.member.model import MemberResponse, MemberModel
from building.client.member.service import MemberService
from utils.database import get_database

member_router = APIRouter(prefix='/building/clients/members', tags=['Buildings', 'Clients', 'Members'])


def get_service(database: Session = Depends(get_database)) -> MemberService:
    return MemberService(database)


@member_router.post('/register', response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create(model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.create(model)


@member_router.patch('/update/{member_id}', response_model=MemberResponse, status_code=status.HTTP_200_OK)
async def update(member_id: int, model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.update(member_id, model)


@member_router.get('/dashboard/get/{token}', response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def get_dashboard_data(token: str, req: Request,  service: MemberService = Depends(get_service)) -> DashboardResponse:
    return service.populate_dashboard(token, str(req.base_url))


# ==============================
# get member for portaria
# ==============================
@member_router.get('/get/{member_id}', response_model=MemberApartmentResponse, status_code=status.HTTP_200_OK)
async def get_member(member_id: int, service: MemberService = Depends(get_service)) -> MemberApartmentResponse:
    return service.find_member(member_id)
