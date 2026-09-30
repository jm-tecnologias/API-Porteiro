from sqlalchemy.orm import Session

from building.database.schemas import MemberCheckInOutSchema
from utils.baseDao import BaseDAO


class MemberCheckInOutDAO(BaseDAO[MemberCheckInOutSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=MemberCheckInOutSchema
        )
