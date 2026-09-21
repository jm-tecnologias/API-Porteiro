from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.client.model import ClientResponse, ClientModel
from building.client.service import ClientService
from utils.database import get_database

client_router = APIRouter(prefix='/building/clients', tags=['Buildings', 'Clients'])


def get_service(database: Session = Depends(get_database)) -> ClientService:
    return ClientService(database)


@client_router.get('/list-all', response_model=list[ClientResponse], status_code=status.HTTP_200_OK)
async def get_clients(service: ClientService = Depends(get_service)) -> list[ClientResponse]:
    return service.list_all()


@client_router.post('/register', response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create(model: ClientModel, service: ClientService = Depends(get_service)) -> ClientResponse:
    return service.create(model)


