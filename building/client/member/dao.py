from sqlalchemy.orm import Session

from building.database.schemas import MemberSchema
from utils.baseDao import BaseDAO


class MemberDAO(BaseDAO[MemberSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=MemberSchema
        )
