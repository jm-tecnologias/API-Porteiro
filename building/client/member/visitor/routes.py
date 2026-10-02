from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.client.member.visitor.VisitorMemberApartmentResponse import VisitorMemberApartmentResponse
from building.client.member.visitor.model import VisitorResponse, VisitorModel
from building.client.member.visitor.service import VisitorService
from utils.database import get_database

admin_visitor_router = APIRouter(prefix='/building/visitors', tags=['Buildings', 'Visitors'])


def get_service(database: Session = Depends(get_database)) -> VisitorService:
    return VisitorService(database)


# ==============================
# get visitor for portaria
# ==============================
@admin_visitor_router.get('/get/{visitor_id}', response_model=VisitorMemberApartmentResponse,
                    status_code=status.HTTP_200_OK)
async def get_member(visitor_id: int, service: VisitorService = Depends(get_service)) -> VisitorMemberApartmentResponse:
    return service.scan_visitor(visitor_id)
