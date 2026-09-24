from sqlalchemy.orm import Session

from building.database.schemas import VisitorSchema
from utils.baseDao import BaseDAO


class VisitorDAO(BaseDAO[VisitorSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=VisitorSchema
        )
        