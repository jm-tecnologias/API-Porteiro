from sqlalchemy.orm import Session

from building.database.schemas import HistoricSchema
from utils.baseDao import BaseDAO


class HistoricDAO(BaseDAO[HistoricSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=HistoricSchema
        )
