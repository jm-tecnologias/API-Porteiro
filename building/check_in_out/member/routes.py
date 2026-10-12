from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.user.employee.permissions import require_permission
from building.check_in_out.member.model import MemberCheckInOutResponse, MemberCheckInOutModel
from building.check_in_out.member.service import MemberCheckInOutService
from utils.database import get_database

admin_member_checkInOut_router = APIRouter(prefix='/building/check-in-out/member',
                                           tags=['Building', 'Member-Check In-Out'])


def get_service(database: Session = Depends(get_database)) -> MemberCheckInOutService:
    return MemberCheckInOutService(database)


@admin_member_checkInOut_router.post('/register', response_model=MemberCheckInOutResponse,
                                     status_code=status.HTTP_201_CREATED)
async def create(model: MemberCheckInOutModel,
                 service: MemberCheckInOutService = Depends(get_service),
                 current_user=Depends(require_permission('MEMBER_CHECK_IN_OUT:CREATE'))) -> MemberCheckInOutResponse:
    return service.create(model)
