from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.occupational_historic.model import HistoricResponse, HistoricApartmentResponse, HistoricModel
from building.occupational_historic.service import HistoricService
from utils.database import get_database

historic_router = APIRouter(prefix='/building/client/historic', tags=['Buildings', 'Clients', 'Histories'])


def get_service(database: Session = Depends(get_database)) -> HistoricService:
    return HistoricService(database)


@historic_router.get('/list-all', response_model=list[HistoricApartmentResponse], status_code=status.HTTP_200_OK)
async def get_historic(service: HistoricService = Depends(get_service)) -> list[HistoricApartmentResponse]:
    return service.list_all()


@historic_router.post('/register', response_model=HistoricResponse, status_code=status.HTTP_201_CREATED)
async def create(model: HistoricModel, service: HistoricService = Depends(get_service)) -> HistoricResponse:
    return service.create(model)


@historic_router.patch('/update/{created_at}', response_model=HistoricResponse, status_code=status.HTTP_200_OK)
async def update(created_at: str, model: HistoricModel, service: HistoricService = Depends(get_service)) -> HistoricResponse:
    return service.update(created_at, model)
