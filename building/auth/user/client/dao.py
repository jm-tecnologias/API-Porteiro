from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import MemberSchema, ClientSchema, ApartmentSchema, BuildingSchema, ContactSchema, \
    AddressSchema
from building.database.schemas.member_user_schema import UserMemberSchema
from utils.baseDao import BaseDAO
from typing import TypeVar
T = TypeVar("T")



class UserMemberDAO(BaseDAO[UserMemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=UserMemberSchema
        )

    def find_by_username(self, username: str) -> UserMemberSchema:
        stmt = select(UserMemberSchema).where(UserMemberSchema.username == username)
        return self.database.scalar(stmt)

    def load_dashboard(self, user_id: int) -> T:
        # stmt = (select(UserMemberSchema, MemberSchema,
        #                # ClientSchema,
        #                ApartmentSchema, BuildingSchema, ContactSchema, AddressSchema)
        #         .join(MemberSchema, UserMemberSchema.member_id == MemberSchema.id)
        #         # .join(ClientSchema, MemberSchema.client_id == ClientSchema.id)
        #         .join(ApartmentSchema, MemberSchema.apartment_id == ApartmentSchema.id)
        #         .join(BuildingSchema, ApartmentSchema.building_id == BuildingSchema.id)
        #         .join(ContactSchema, BuildingSchema.id == ContactSchema.building_id)
        #         .join(AddressSchema, BuildingSchema.id == AddressSchema.building_id)
        #         ).where(UserMemberSchema.id == user_id)
        # # return self.database.execute(stmt).first()
        # return self.database.execute(stmt).all()
        # # return self.database.scalar(stmt)
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
