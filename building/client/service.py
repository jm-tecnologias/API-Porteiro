from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from building.client.dao import ClientDAO
from building.client.model import ClientResponse, ClientModel
from building.database.schemas.client_schema import ClientSchema


class ClientService:
    def __init__(self, database: Session):
        self.dao = ClientDAO(database)

    def create(self, client_data: ClientModel) -> ClientResponse:
        # the surname should be for example: Mula, Amilcar
        client = self.dao.find_by_surname(client_data.surname)
        if client:
            if client.status:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Client Already Exist!')
        new = ClientSchema(
            user_id=client_data.user_id,
            surname=client_data.surname,
            num_members=client_data.num_members,
            description=client_data.description,
            building_id=client_data.building_id
        )
        try:
            return self.dao.create(new)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Data Structure Not Valid!')

    def update(self, client_id: int, client_data: ClientModel) -> ClientResponse:
        client = self.dao.find_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client Not Found!')
        data = client_data.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(client, field, value)
        try:
            return self.dao.update(client)
        except SQLAlchemyError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail='Was Not Possible To Update Data!')

    def list_all(self) -> list[ClientResponse]:
        return self.dao.find_all()

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = ClientService(database)
#     data = ClientModel(
#         user_id=15,
#         surname="Mula Jr",
#         description="Primeiro Cliente: actualizado",
#         num_members=3,
#         building_id=1,
#         status=True
#     )
#     user = service.create(data)
#
#     # clients = service.list_all()
#     # for client in clients:
#     #     print(client.description)
#     # service.update(1, data)
# finally:
#     database.close()
