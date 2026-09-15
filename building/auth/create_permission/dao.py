from sqlalchemy import select
from sqlalchemy.orm import Session
from building.database.schemas import PermissionSchema
from utils.baseDao import BaseDAO


class PermissionDAO(BaseDAO[PermissionSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=PermissionSchema
        )

    def check_permission(self, module: str, action: str) ->PermissionSchema:
        stmt = (select(PermissionSchema).where(PermissionSchema.module == module)
                .where(PermissionSchema.action == action))
        return self.database.scalar(stmt)
