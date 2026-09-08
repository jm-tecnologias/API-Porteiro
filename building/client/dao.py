from sqlalchemy.orm import Session

from building.database.schemas.client_schema import ClientSchema
from utils.baseDao import BaseDAO


class ClientDAO(BaseDAO[ClientSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=ClientSchema
        )
