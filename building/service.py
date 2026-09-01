from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.dao import BuildingDAO
from building.model import BuildingModel, BuildingResponse
from utils.schemas.building_schema import BuildingSchema


class BuildingService:
    def __init__(self, database: Session):
        # self.database = database
        self.dao = BuildingDAO(database)

    def create(self, build: BuildingModel) -> BuildingResponse:
        building = self.dao.find_by_name(build.name)
        if building:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Building name already exist!')

        new = BuildingSchema(
            name=build.name,
            description=build.description
        )
        return self.dao.create(new)

    def update(self, build_id: int, build_data: BuildingModel) -> BuildingResponse:
        building = self.dao.find_by_id(build_id)
        if not building:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found!')
        data = build_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(building, field, value)
        try:
            return self.dao.update(building)
        except InterruptedError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was not possible to update data.')

    def find_all_buildings(self, status: bool = None) -> list[BuildingResponse]:
        buildings = self.dao.find_all()
        building_list = []
        for build in buildings:
            if status is not None:
                if build.status == status:
                    building_list.append(build)
        if status is not None:
            return building_list
        return buildings

from utils.database import SessionLocal
database = SessionLocal()
# ========= Create =========
# try:
#     service = BuildingService(database)
#     data = BuildingSchema(
#          name="JAT35",
#          description="Dados de teste",
#          status=True
#     )
#     build = service.create(data)
# print('Build Created:')
# print('ID: ', build.id)
# print('Name: ', build.name)
# print('Description: ', build.description)
# print('Status: ', build.status)
# print('Created at: ', build.created_at)
# print('Updated at: ', build.updated_at)
# print('Contacts: ', build.contacts)
# print('__________________________________________________________________')
# print(' ')
# finally:
#     database.close()


# ========= List All =========
# try:
#     service = BuildingService(database)
#     buildings = service.find_all_buildings()
#     for build in buildings:
#         print('Building ')
#         print('ID: ', build.id)
#         print('Name: ', build.name)
#         print('Description: ', build.description)
#         print('Status: ', build.status)
#         print('Created at: ', build.created_at)
#         print('Updated at: ', build.updated_at)
#         print('Contacts: ', build.contacts)
#         print('departments: ', build.departments)
#         print('employees: ', build.employees)
#         print('apartments: ', build.apartments)
#         print('clients: ', build.clients)
#         print('__________________________________________________________________')
#         print(' ')
# finally:
#     database.close()
