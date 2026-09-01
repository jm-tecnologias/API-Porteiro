from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.contact.dao import ContactDAO
from building.contact.model import ContactResponse, ContactModel
from building.dao import BuildingDAO
from utils.schemas.building_schema import ContactSchema


class ContactService:
    def __init__(self, database: Session):
        self.dao = ContactDAO(database)
        self.dao_build = BuildingDAO(database)

    def create(self, contact_data: ContactModel) -> ContactResponse:
        contact = self.dao.find_by_phone(contact_data.phone)
        if contact:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Phone number already exist!')
        contact = self.dao.find_by_email(contact_data.email)
        if contact:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exist!')
        building = self.dao_build.find_by_id(contact_data.building_id)
        if not building.status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not Allowed!')

        new = ContactSchema(
            phone=contact_data.phone,
            website=contact_data.website,
            email=contact_data.email,
            building_id=contact_data.building_id
        )
        return self.dao.create(new)

    def update(self, contact_id: int, contact_data: ContactModel) -> ContactResponse:
        contact = self.dao.find_by_id(contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data Not Found!')
        data = contact_data.model_dump(exclude_unset=True)
        if "phone" in data:
            phone = data["phone"]
            contact = self.dao.find_by_phone(phone)
            if contact:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Phone Number already exist!')
        if "email" in data:
            email = data["email"]
            contact = self.dao.find_by_email(email)
            if contact:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exist!')
        if "website" in data:
            website = data["website"]
            contact = self.dao.find_by_website(website)
            if contact:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='website already exist!')

        for field, value in data.items():
            setattr(contact, field, value)
        try:
            return self.dao.update(contact)
        except InterruptedError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Update Data')

    def find_all(self, building_id: int, skip: int, limit: int, status: bool = None) -> list[ContactResponse]:
        contacts = self.dao.list_contacts(building_id=building_id, skip=skip, limit=limit)
        contact_list = []
        for contact in contacts:
            if status is not None:
                if contact.status == status:
                    contact_list.append(contact)
        if status is not None:
            return contact_list
        return contacts
