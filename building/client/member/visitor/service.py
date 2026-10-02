from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from building.apartment.model import ApartmentResponse
from building.barcode_service import BarcodeService
from building.client.member.model import MemberResponse
from building.client.member.visitor.VisitorMemberApartmentResponse import VisitorMemberApartmentResponse
from building.client.member.visitor.dao import VisitorDAO
from building.client.member.visitor.model import VisitorResponse, VisitorModel
from building.database.schemas import VisitorSchema


class VisitorService:
    def __init__(self, database: Session):
        self.dao = VisitorDAO(database)

    def scan_visitor(self, visitor_id: int) -> VisitorMemberApartmentResponse:
        data = self.dao.find_visitor(visitor_id)
        vi, me, ap = data
        return VisitorMemberApartmentResponse(
            visitor=VisitorResponse(
                member_id=vi.member_id,
                name=vi.name,
                phone=vi.phone,
                visitor_date=vi.visitor_date,
                visitor_time=vi.visitor_time,
                status=vi.status,
                description=vi.description,
                id=vi.id,
                token=vi.token,
                created_at=vi.created_at,
                updated_at=vi.updated_at,
                visitor_check_historic=vi.visitor_check_historic
            ),
            member=MemberResponse(
                user_id=me.user_id,
                client_id=me.client_id,
                apartment_id=me.apartment_id,
                doc_id=me.doc_id,
                name=me.name,
                surname=me.surname,
                phone=me.phone,
                email=me.email,
                client_relationship=me.client_relationship,
                description=me.description,
                status=me.status,
                profile_pic_url=me.profile_pic_url,
                # barcode_url
                id=me.id,
                token=me.token,
                created_at=me.created_at,
                updated_at=me.updated_at,
                # visitors=me.visitors,
                # checkedStatus=me.checkedStatus
            ),
            apartment=ApartmentResponse(
                floor=ap.floor,
                number=ap.number,
                type=ap.type,
                description=ap.description,
                occupation_state=ap.occupation_state,
                building_id=ap.building_id,
                status=ap.status,
                id=ap.id,
                created_at=ap.created_at,
                updated_at=ap.updated_at
            )
        )
# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = VisitorService(database)
#     model = VisitorModel(
#         member_id=1,
#         name='sdfgd Mula Jr.',
#         phone='847100793',
#         visitor_date='2026-09-24',
#         visitor_time='16:00',
#         description='Visita de uma Semana'
#     )
#     model = service.create(model)
#     print(model)
#     data = service.find_visitor(1)
#     print(data)
# finally:
#    database.close()
