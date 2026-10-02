from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import MemberSchema, ApartmentSchema, UserMemberSchema, ContactSchema, AddressSchema, \
    BuildingSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")


class MemberDAO(BaseDAO[MemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=MemberSchema
        )

    def load_dashboard(self, user_id: int) -> T:
        stmt = (
            select(UserMemberSchema, MemberSchema, ApartmentSchema, BuildingSchema,
                ContactSchema, AddressSchema)
            .join(MemberSchema, UserMemberSchema.member_id == MemberSchema.id)
            .join(ApartmentSchema, MemberSchema.apartment_id == ApartmentSchema.id)
            .join(BuildingSchema, ApartmentSchema.building_id == BuildingSchema.id)
            .join(ContactSchema, BuildingSchema.id == ContactSchema.building_id)
            .join(AddressSchema, BuildingSchema.id == AddressSchema.building_id)
            .where(UserMemberSchema.id == user_id))
        return self.database.execute(stmt).one_or_none()

    def find_member(self, member_id: int) -> T:
        stmt = (
            select(MemberSchema, ApartmentSchema)
            .join(ApartmentSchema, MemberSchema.apartment_id == ApartmentSchema.id)
            .where(MemberSchema.id == member_id))
        return self.database.execute(stmt).one_or_none()
