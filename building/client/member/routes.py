from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from building.client.member.MemberApartmentResponse import MemberApartmentResponse
from building.client.member.model import MemberResponse, MemberModel
from building.client.member.service import MemberService
from utils.database import get_database

admin_member_router = APIRouter(prefix='/building/clients/members', tags=['Buildings', 'Clients', 'Members'])


def get_service(database: Session = Depends(get_database)) -> MemberService:
    return MemberService(database)


@admin_member_router.post('/register', response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create(model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.create(model)


@admin_member_router.patch('/update/{member_id}', response_model=MemberResponse, status_code=status.HTTP_200_OK)
async def update(member_id: int, model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.update(member_id, model)


# ==============================
# get member for portaria
# ==============================
@admin_member_router.get('/get/{token}', response_model=MemberApartmentResponse, status_code=status.HTTP_200_OK)
async def get_member(token: str, req: Request,
                     service: MemberService = Depends(get_service)) -> MemberApartmentResponse:
    return service.scan_member(token, str(req.base_url))
