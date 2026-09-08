from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.address.dao import AddressDAO
from building.address.model import AddressResponse, AddressModel
from building.dao import BuildingDAO
from building.database.schemas.building_schema import AddressSchema


class AddressService:
    def __init__(self, database: Session):
        self.dao = AddressDAO(database)
        self.dao_building = BuildingDAO(database)

    def create(self, address_data: AddressModel) -> AddressResponse:
        address = self.dao.find_by_number(address_data.number)
        if address:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Address or Number Already exist!')
        new = AddressSchema(
            building_id=address_data.building_id,
            province=address_data.province,
            avenue=address_data.avenue,
            number=address_data.number,
            nearby_hood=address_data.nearby_hood,
            city=address_data.city
        )
        return self.dao.create(new)

    def update(self, address_id: int, address_data: AddressModel) -> AddressResponse:
        address = self.dao.find_by_id(address_id)
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data Not Found!')
        data = address_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(address, field, value)

        try:
            return self.dao.update(address)
        except InterruptedError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Update Data!')

    def find_building_address(self, building_id: int) -> AddressResponse | None:
        building = self.dao_building.find_by_id(building_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data Not Found!')
        address = self.dao.find_address(building_id=building_id)
        if address is not None:
            return address
        return None


# from utils.database import SessionLocal
# database = SessionLocal()

# try:
#     service = AddressService(database)
#     data = AddressSchema(
#         building_id=1,
#         province="Maputo",
#         number=211,
#         avenue="Av. Patrice Lumumba",
#         nearby_hood="PL City",
#         city="Matola",
#     )
#     address = service.create(data)
#     print("Address created:")
#     print('Build Created:')
#     print('ID: ', address.id)
#     print('Province: ', address.province)
#     print('City: ', address.city)
#     print('Avenue: ', address.avenue)
#     print('Nearby Hood: ', address.nearby_hood)
#     print('Status: ', address.status)
#     print('Created at: ', address.created_at)
#     print('Updated at: ', address.updated_at)
# finally:
#     database.close()

# try:
#     service = AddressService(database)
#     data = AddressModel(
#         # province="Maputo",
#         # number=211,
#         avenue="Av. Patrice Lumumba",
#         nearby_hood="PL City",
#         city="Cidade da Matola",
#     )
#     address = service.update(1, data)
#     print("Address created:")
#     print('Build Created:')
#     print('ID: ', address.id)
#     print('Province: ', address.province)
#     print('City: ', address.city)
#     print('Number: ', address.number)
#     print('Avenue: ', address.avenue)
#     print('Nearby Hood: ', address.nearby_hood)
#     print('Status: ', address.status)
#     print('Created at: ', address.created_at)
#     print('Updated at: ', address.updated_at)
# finally:
#     database.close()

# try:
#     service = AddressService(database)
#     address = service.find_building_address(2)
#     if address:
#         print("Address: ", address)
#         print('ID: ', address.id)
#         print('Province: ', address.province)
#         print('City: ', address.city)
#         print('Avenue: ', address.avenue)
#         print('Nearby Hood: ', address.nearby_hood)
#         print('Status: ', address.status)
#         print('Created at: ', address.created_at)
#         print('Updated at: ', address.updated_at)
# finally:
#     database.close()
