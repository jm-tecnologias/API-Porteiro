from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.apartment.model import ApartmentResponse, ApartmentModel
from building.apartment.service import ApartmentService
from utils.database import get_database

apartment_router = APIRouter(prefix='/building/apartment', tags=['Buildings', 'Apartments'])


def get_service(database: Session = Depends(get_database)) -> ApartmentService:
    return ApartmentService(database)


@apartment_router.get('/list-all', response_model=list[ApartmentResponse], status_code=status.HTTP_200_OK)
async def list_all(service: ApartmentService = Depends(get_service)) -> list[ApartmentResponse]:
    return service.list_all()


@apartment_router.post('/register', response_model=ApartmentResponse, status_code=status.HTTP_201_CREATED)
async def register(ap: ApartmentModel, service: ApartmentService = Depends(get_service)) -> ApartmentResponse:
    return service.create(ap)


@apartment_router.patch('/update/{apartment_id}', response_model=ApartmentResponse,
                        status_code=status.HTTP_201_CREATED)
async def update(apartment_id: int, apartment: ApartmentModel,
                 service: ApartmentService = Depends(get_service)) -> ApartmentResponse:
    return service.update(apartment_id, apartment)
