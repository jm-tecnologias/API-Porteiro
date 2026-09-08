from sqlalchemy import select
from sqlalchemy.orm import Session

from building.database.schemas import ProfilePermissionSchema
from utils.baseDao import BaseDAO


class ProfilePermissionDAO(BaseDAO[ProfilePermissionSchema]):
    def __init__(self, database: Session):
        super().__init__(
            database=database,
            model=ProfilePermissionSchema
        )

    def check_profile_permission(self, profile_id: int, permission_id: int) -> ProfilePermissionSchema:
        stmt = (select(ProfilePermissionSchema).where(ProfilePermissionSchema.profile_id == profile_id)
                .where(ProfilePermissionSchema.permission_id == permission_id)
                .where(ProfilePermissionSchema.status == 1))
        return self.database.scalar(stmt)
