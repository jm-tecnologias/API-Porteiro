from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from building.contact.model import ContactResponse, ContactModel
from building.contact.service import ContactService
from utils.database import get_database

contact_router = APIRouter(prefix='/building/contact', tags=['Buildings', 'Contacts'])


def get_contact_service(database: Session = Depends(get_database)) -> ContactService:
    return ContactService(database)


@contact_router.get('/find-all/{build_id}/{status}', response_model=list[ContactResponse],
                    status_code=status.HTTP_200_OK)
async def get_all(build_id: int, status: bool = None,
                  skip: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=500),
                  service: ContactService = Depends(get_contact_service)) -> list[ContactResponse]:
    return service.find_all(building_id=build_id, skip=skip, limit=limit, status=status)


@contact_router.post('/register', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create(contact: ContactModel, service: ContactService = Depends(get_contact_service)) -> ContactResponse:
    return service.create(contact)


@contact_router.patch('/update/{contact_id}', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def update(contact_id: int, contact: ContactModel,
                 service: ContactService = Depends(get_contact_service)) -> ContactResponse:
    return service.update(contact_id=contact_id, contact_data=contact)
