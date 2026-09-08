from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from building.database.schemas.profile_schema import ProfileSchema


class ProfileDAO(BaseDAO[ProfileSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=ProfileSchema
        )
