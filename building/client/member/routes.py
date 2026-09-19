from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.client.member.model import MemberResponse, MemberModel
from building.client.member.service import MemberService
from utils.database import get_database

member_router = APIRouter(prefix='/building/clients/members', tags=['Buildings', 'Clients', 'Members'])


def get_service(database: Session = Depends(get_database)) -> MemberService:
    return MemberService(database)


@member_router.post('/register', response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create(model: MemberModel, service: MemberService = Depends(get_service)) -> MemberResponse:
    return service.create(model)
