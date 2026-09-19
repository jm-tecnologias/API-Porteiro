from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from building.apartment.model import ApartmentResponse
from building.client.dao import ClientDAO
from building.database.schemas import HistoricSchema
from building.occupational_historic.dao import HistoricDAO
from building.occupational_historic.model import HistoricResponse, HistoricModel, HistoricApartmentResponse


class HistoricService:
    def __init__(self, database: Session):
        self.dao = HistoricDAO(database)
        self.dao_client = ClientDAO(database)

    def create(self, model: HistoricModel) -> HistoricResponse:
        client = self.dao_client.find_by_id(model.client_id)
        if client:
            if client.status:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                    detail='Client Is No Longer Active!')
        new = HistoricSchema(
            client_id=model.client_id,
            user_id=model.user_id,
            apartment_id=model.apartment_id,
            occupational_date=model.occupational_date,
            final_date=model.final_date,
            description=model.description,
            num_members=model.num_members
        )
        try:
            return self.dao.create(new)
        except InterruptedError:
            self.dao.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Was Not Possible To Add Data!')

    def list_all(self) -> list[HistoricApartmentResponse]:
        data = self.dao.list_all()
        if data is None:
            return None
        historic_apartment = []
        for parts in data:
            hist, ap = parts
            historic_apartment.append(HistoricApartmentResponse(
                historic=HistoricResponse(
                    client_id=hist.client_id,
                    apartment_id=hist.apartment_id,
                    occupational_date=hist.occupational_date,
                    final_date=hist.final_date,
                    description=hist.description
                ),
                apartment=ApartmentResponse(
                    id=ap.id,
                    floor=ap.floor,
                    number=ap.number,
                    type=ap.type,
                    occupation_state=ap.occupation_state,
                    description=ap.description
                )
            ))
        return historic_apartment



# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = HistoricService(database)
#     data = HistoricModel(
#         client_id=1,
#         user_id=1,
#         apartment_id=1,
#         occupational_date='2026-09-01',
        # final_date=model.final_date,
        # description='Segunda Ocupacao',
        # num_members=8
    # )
    # service.create(data)
    # data_set = service.list_all()
    # print(data_set)
    # for historic, apartment in data_set:
    #     print('Client id: ', historic.client_id)
    #     print(apartment.number)
#
# finally:
#     database.close()
