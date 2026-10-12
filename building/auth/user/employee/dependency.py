from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from utils.database import get_database
from utils.auth_service import AuthService
from building.auth.user.employee.dao import UserEmployeeDAO

security = HTTPBearer(auto_error=True)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        database: Session = Depends(get_database),
):
    auth_service = AuthService(
        database=database,
        dao_class=UserEmployeeDAO,
    )

    token = credentials.credentials

    return auth_service.verify_token(token)
