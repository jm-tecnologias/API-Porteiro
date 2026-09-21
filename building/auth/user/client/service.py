from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.auth.user.client.dao import UserMemberDAO
from building.auth.user.client.model import UserMemberModel, UserMemberResponse, LoginResponse, TokenResponse, \
    DashboardResponse, DashboardUserResponse, DashboardMemberResponse, DashboardApartmentResponse, \
    DashboardBuildingResponse, DashboardContactResponse, DashboardAddressResponse
from building.client.member.dao import MemberDAO
from building.database.schemas.member_user_schema import UserMemberSchema
from typing import TypeVar, Generic, Type
T = TypeVar("T")

from jose import jwt, JWTError
import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = str(os.getenv("TOKEN_EXPIRE_MINUTES"))


class UserMemberService:
    def __init__(self, database: Session):
        self.dao = UserMemberDAO(database)
        self.dao_member = MemberDAO(database)

    def create(self, user_data: UserMemberModel) -> UserMemberResponse:
        checked_user = self.dao.find_by_username(user_data.username)
        if checked_user:
            if checked_user.status:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User Already Exist!')
        client = self.dao_member.find_by_id(user_data.member_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data(Employee) Not Found!')
        if client:
            if not client.status:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Employee Is Disable')

        new = UserMemberSchema(
            description=user_data.description,
            status=user_data.status,
            member_id=user_data.member_id,
            password=self._hash_password(user_data.password),
            username=user_data.username
        )
        return self.dao.create(new)

    # def get_user_login(self, username: str, password: str) -> LoginResponse:

    def get_user_login(self, username: str, password: str) -> TokenResponse:
        user = self.dao.find_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif not self._verify_password(password, user.password):
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

        access_token = self.create_token(login.id, login)
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
        # res = LoginResponse.model_validate(login)
        # return res.model_copy(
        #     update={"token": self.create_token(res.id, res)}
        # )
        # return login

    def populate_dashboard(self, user_id: str) -> DashboardResponse:
        logged_user = self.verify_token(user_id)
        # Tratamento de erro se o login nao existir
        data = self.dao.load_dashboard(logged_user.id)
        if data is None:
            return None
        user, member, apartment, building, contact, address = data
        return DashboardResponse(
            user=DashboardUserResponse(
                id=user.id,
                username=user.username,
                description=user.description,
                status=user.status
            ),
            member=DashboardMemberResponse(
                id=member.id,
                doc_id=member.doc_id,
                name=member.name,
                surname=member.surname,
                phone=member.phone,
                email=member.email,
                description=member.description,
                status=member.status
            ),
            apartment=DashboardApartmentResponse(
                id=apartment.id,
                floor=apartment.floor,
                number=apartment.number,
                type=apartment.type,
                description=apartment.description,
                status=apartment.status,
                occupation_state=apartment.occupation_state
            ),
            building=DashboardBuildingResponse(
                id=building.id,
                name=building.name,
                status=building.status,
                description=building.description
            ),
            contact=DashboardContactResponse(
                id=contact.id,
                phone=contact.phone,
                email=contact.email,
                website=contact.website,
                status=contact.status
            ),
            address=DashboardAddressResponse(
                id=address.id,
                province=address.province,
                city=address.city,
                nearby_hood=address.nearby_hood,
                avenue=address.avenue,
                number=address.number,
                status=address.status
            )
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt(rounds=12),
        )
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def _verify_password(password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8"),
        )

    @staticmethod
    def create_token(user_id: int, user_log: LoginResponse, token_duration=timedelta(minutes=int(TOKEN_EXPIRE_MINUTES)),
                     token_type="access") -> str:
        token_date_expires = datetime.now(timezone.utc) + token_duration
        token_json = {
            "sub": str(user_id),
            "type": token_type,
            "exp": token_date_expires,
            "iat": datetime.now(timezone.utc),
            # 'extra_logs': user_log
            # "role": user.user_type,
        }
        return jwt.encode(token_json, SECRET_KEY, ALGORITHM)

    def verify_token(self, token: str, expected_type: str = "access"):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != expected_type:
                raise ValueError
            user_id = int(str(payload.get("sub")))

            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token without user ID")

            # user_id = int(user_id)

        except (JWTError, TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired")

        user = self.dao.find_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token user not found")
        return user

# from utils.database import SessionLocal
# from building.database import models
# database = SessionLocal()
# try:
#     service = UserMemberService(database)
#     to = service.verify_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc5MDAwNzA5MSwiaWF0IjoxNzkwMDA1MjkxfQ.p3FiAHJ7JGR_ts85PFtwN42GITDUU__mTm7zf3NOZvU')
#     print('Result: ', to.username)
#     data = UserMemberModel(
#         username="Client",
#         password="Informatico@12",
#         description="Test User",
#         member_id=1,
#         status=True
#     )
#     # user = service.create(data)
#     user = service.get_user_login('Client', 'Informatico@12')
#     print(user)
#     data_set = service.populate_dashboard(1)
#     print(type(data_set))
#     print(data_set)
    # for dados in data_set:
    #     print(dados[0])
    # if data_set:
    #     user, member, client, apartment, building, contact, address = data_set
    # for user, member, client, apartment, building, contact, address in data_set:
    #     print(type(user))
    #     print(user.username)
    #     print(member.name)
    #     print(client.surname)
    #     print(apartment.floor)
    #     print(building.name)
    #     print(contact.phone)
    #     print(address.province)
    # else:
    #     print("Utilizador não encontrado.")
    # print(user.username)
    # print(user.description)
    # print(user.member_id)
    # print(user.status)
    # print(user.created_at)
    # print(user.updated_at)
    # print(user.token)
# finally:
#     database.close()
