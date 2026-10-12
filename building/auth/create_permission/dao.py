from sqlalchemy import select
from sqlalchemy.orm import Session
from building.database.schemas import PermissionSchema, ProfilePermissionSchema, UserProfileEmployeeSchema
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

    def has_permission(self, user_id: int, permission_code: str):
        stmt = (select(PermissionSchema, ProfilePermissionSchema, UserProfileEmployeeSchema)
                .join(
            ProfilePermissionSchema, ProfilePermissionSchema.permission_id == PermissionSchema.id)
                .join(
            UserProfileEmployeeSchema, UserProfileEmployeeSchema.profile_id == ProfilePermissionSchema.profile_id)
                .where(UserProfileEmployeeSchema.employee_user_id == user_id)
                .where(PermissionSchema.code == permission_code))

        return self.database.execute(stmt).first()
