from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from building.client.member.visitor.VisitorMemberApartmentResponse import VisitorMemberApartmentResponse, \
    VisitorMemberResponse
from building.client.member.visitor.model import VisitorResponse, VisitorModel
from building.client.member.visitor.service import VisitorService
from utils.database import get_database

admin_visitor_router = APIRouter(prefix='/building/visitors', tags=['Buildings', 'Visitors'])


def get_service(database: Session = Depends(get_database)) -> VisitorService:
    return VisitorService(database)


# ==============================
# get visitor for portaria
# ==============================
@admin_visitor_router.get('/get/{token}', response_model=VisitorMemberApartmentResponse,
                          status_code=status.HTTP_200_OK)
async def get_visitor(token: str, req: Request,
                      service: VisitorService = Depends(get_service)) -> VisitorMemberApartmentResponse:
    return service.scan_visitor(token, str(req.base_url))


@admin_visitor_router.get('/list-all', response_model=list[VisitorMemberResponse], status_code=status.HTTP_200_OK)
async def list_all_visitors(service: VisitorService = Depends(get_service)) -> list[VisitorMemberResponse]:
    return service.list_all()
