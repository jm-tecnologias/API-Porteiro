from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.auth.user.employee.permissions import require_permission
from building.check_in_out.visitor.model import VisitorCheckInOutResponse, VisitorCheckInOutModel
from building.check_in_out.visitor.service import VisitorCheckInOutService
from utils.database import get_database

admin_visitor_checkInOut_router = APIRouter(prefix='/building/check-in-out/visitor',
                                            tags=['Building', 'Visitor-Check In-Out'])


def get_service(database: Session = Depends(get_database)) -> VisitorCheckInOutService:
    return VisitorCheckInOutService(database)


@admin_visitor_checkInOut_router.post('/register', response_model=VisitorCheckInOutResponse,
                                      status_code=status.HTTP_201_CREATED)
async def create(model: VisitorCheckInOutModel,
                 service: VisitorCheckInOutService = Depends(get_service),
                 current_user=Depends(require_permission('VISITOR_CHECK_IN_OUT:CREATE'))) -> VisitorCheckInOutResponse:
    return service.create(model)
