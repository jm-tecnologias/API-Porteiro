
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from utils.database import get_database
from building.auth.create_permission.service import PermissionService
from building.auth.user.employee.dependency import get_current_user


def require_permission(permission_code: str):
    def dependency(
        current_user=Depends(get_current_user),
        database: Session = Depends(get_database),
    ):
        permission_service = PermissionService(database)

        has_permission = permission_service.has_permission(
            user_id=current_user.id,
            permission_code=permission_code,
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não tens permissão para executar esta operação.",
            )

        return current_user

    return dependency
