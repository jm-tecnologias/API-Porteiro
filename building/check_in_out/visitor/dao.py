from sqlalchemy.orm import Session

from building.database.schemas import VisitorCheckInOutSchema
from utils.baseDao import BaseDAO


class VisitorCheckInOutDAO(BaseDAO[VisitorCheckInOutSchema]):

    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=VisitorCheckInOutSchema)
        