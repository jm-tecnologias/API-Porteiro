from sqlalchemy.orm import Session

from building.database.schemas import OrdinaryVisitorSchema
from utils.baseDao import BaseDAO


class OrdinaryVisitorDAO(BaseDAO[OrdinaryVisitorSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=OrdinaryVisitorSchema
        )
