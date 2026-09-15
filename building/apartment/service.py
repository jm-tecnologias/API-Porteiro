from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.apartment.dao import ApartmentDAO
from building.apartment.model import ApartmentResponse, ApartmentModel
from building.dao import BuildingDAO
from building.database.schemas.apartment_schema import ApartmentSchema


class ApartmentService:
    def __init__(self, database: Session):
        self.dao = ApartmentDAO(database)
        self.dao_build = BuildingDAO(database)

    def create(self, ap: ApartmentModel) -> ApartmentResponse:
        building = self.dao_build.find_by_id(ap.building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data Not Found!')
        apartment = self.dao.find_by_number(ap.number, ap.building_id)
        if apartment:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Apartment Number Already Exist!')
        new = ApartmentSchema(
            floor=ap.floor,
            number=ap.number,
            building_id=ap.building_id,
            description=ap.description,
            occupation_state=ap.occupation_state,
            _type=ap.type,
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Data Structure Not Valid!')

    def update(self, ap_id: int, ap_data: ApartmentModel) -> ApartmentResponse:
        apartment = self.dao.find_by_id(ap_id)
        if not apartment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Apartment Not Found!')
        data = ap_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(apartment, field, value)
        try:
            return self.dao.update(apartment)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Update Data!')

    def list_all(self) -> list[ApartmentResponse]:
        return self.dao.find_all()


# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = ApartmentService(database)
#     ap = ApartmentModel(
#         floor="5",
#         number="A212",
#         type="T2",
#         description="Apartamento tipo 2 para casal",
#         building_id=1,
#     )
#     ap = service.create(ap)
#     print('Apartment Created')
#     print('ID: ', ap.id)
#     print('Floor: ', ap.floor)
#     print('Number: ', ap.number)
#     print('Type: ', ap.type)
#     print('Description: ', ap.description)
#     print('Building ID: ', ap.building_id)
#     print('Status: ', ap.status)
# finally:
#     database.close()

# try:
#     service = ApartmentService(database)
#
#     apartments = service.list_all()
#     for ap in apartments:
#         print('Apartment Created')
#         print('ID: ', ap.id)
#         print('Floor: ', ap.floor)
#         print('Number: ', ap.number)
#         print('Type: ', ap.type)
#         print('Description: ', ap.description)
#         print('Building ID: ', ap.building_id)
#         print('Status: ', ap.status)
#         print('Created at: ', ap.created_at)
#         print('Updated at: ', ap.updated_at)
# finally:
#     database.close()

# try:
#     service = ApartmentService(database)
#     ap = ApartmentModel(
#         floor="5",
#         number="B222"
#     )
#     ap = service.update(2, ap)
#     print('Apartment Created')
#     print('ID: ', ap.id)
#     print('Floor: ', ap.floor)
#     print('Number: ', ap.number)
#     print('Type: ', ap.type)
#     print('Description: ', ap.description)
#     print('Building ID: ', ap.building_id)
#     print('Status: ', ap.status)
# finally:
#     database.close()
