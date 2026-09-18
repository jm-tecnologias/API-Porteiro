from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from building.client.model import ClientResponse
from building.client.service import ClientService
from utils.database import get_database

client_router = APIRouter(prefix='/building/clients', tags=['Buildings', 'Clients'])


def get_service(database: Session = Depends(get_database)) -> ClientService:
    return ClientService(database)


@client_router.get('/list-all', response_model=list[ClientResponse], status_code=status.HTTP_200_OK)
async def get_clients(service: ClientService = Depends(get_service)) -> list[ClientResponse]:
    return service.list_all()
