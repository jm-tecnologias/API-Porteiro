from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from client.auth.user.client.dao import UserMemberDAO
from client.auth.user.client.model import TokenResponse, LoginResponse
from utils.auth_service import AuthService


class UserMemberService:
    def __init__(self, database: Session):
        self.dao = UserMemberDAO(database)
        self.auth_helper = AuthService(database=database, model=UserMemberDAO)

    def get_user_login(self, username: str, password: str) -> TokenResponse:
        user = self.dao.find_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif not self.auth_helper.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is incorrect")
        login = LoginResponse(
            id=user.id,
            username=user.username,
            description=user.description,
            member_id=user.member_id,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        # history_data = UserHistoryCreate(
        #     user_id=user.id,
        #     action="LOGIN"
        # )
        # self.history_service.create_history(history_data)

        access_token = self.auth_helper.create_token(login.id)
        print('TOKEN: ', access_token)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
