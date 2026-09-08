from sqlalchemy.orm import Session

from utils.baseDao import BaseDAO
from building.database.schemas.building_schema import BuildingSchema


class BuildingDAO(BaseDAO[BuildingSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=BuildingSchema
        )
