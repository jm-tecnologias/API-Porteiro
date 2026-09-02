from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.address.model import AddressResponse, AddressModel
from building.address.service import AddressService
from utils.database import get_database

address_router = APIRouter(prefix='/building/address', tags=['Buildings', 'Address'])


def get_service(database: Session = Depends(get_database)) -> AddressService:
    return AddressService(database)


@address_router.get('/get/{building_id}', response_model=AddressResponse,
                    status_code=status.HTTP_200_OK)
async def get(building_id: int, service: AddressService = Depends(get_service)) -> AddressResponse:
    return service.find_building_address(building_id)


@address_router.post('/register', response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create(address_data: AddressModel, service: AddressService = Depends(get_service)) -> AddressResponse:
    return service.create(address_data)


@address_router.patch('/update/{address_id}', response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def update(address_id: int, address_data: AddressModel, service: AddressService = Depends(get_service)) -> AddressResponse:
    return service.update(address_id=address_id, address_data=address_data)
