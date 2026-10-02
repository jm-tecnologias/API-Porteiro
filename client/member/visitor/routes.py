from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from client.member.visitor.model import VisitorResponse, VisitorModel
from client.member.visitor.service import VisitorService
from utils.database import get_database

visitor_router = APIRouter(prefix='/building/visitors', tags=['Buildings', 'Visitors'])


def get_service(database: Session = Depends(get_database)) -> VisitorService:
    return VisitorService(database)


@visitor_router.post('/register', response_model=VisitorResponse, status_code=status.HTTP_200_OK)
async def create(model: VisitorModel, service: VisitorService = Depends(get_service)) -> VisitorResponse:
    return service.create(model)
