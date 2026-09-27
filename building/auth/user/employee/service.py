from building.database.schemas.employee_user_schema import UserEmployeeSchema
from building.auth.create_profile.dao import ProfileDAO
from building.rh.employee.dao import EmployeeDAO
from building.auth.user.employee.dao import UserEmployeeDAO
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from dotenv import load_dotenv
import os

from building.auth.user.employee.model import UserEmployeeResponse, UserEmployeeModel, ModelLogin, UserEmployee
from building.rh.employee.model import EmployeeResponse

load_dotenv()

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = str(os.getenv("ALGORITHM"))
TOKEN_EXPIRE_MINUTES = str(os.getenv("TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_HOURS = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", "8"))


class UserEmployeeService:
    def __init__(self, database: Session):
        self.dao = UserEmployeeDAO(database)
        self.dao_employee = EmployeeDAO(database)
        self.dao_profile = ProfileDAO(database)

    def create(self, user_data: UserEmployeeModel) -> UserEmployeeResponse:
        checked_user = self.dao.find_by_username(user_data.username)
        if checked_user:
            if checked_user.status:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User Already Exist!')
        employee = self.dao_employee.find_by_id(user_data.employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data(Employee) Not Found!')
        if employee:
            if not employee.status:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Employee Is Disable')

        new = UserEmployeeSchema(
            description=user_data.description,
            status=user_data.status,
            employee_id=user_data.employee_id,
            password=self._hash_password(user_data.password),
            # profile_id=user_data.profile_id,
            username=user_data.username
        )
        return self.dao.create(new)

    def get_user_login(self, username: str, password: str) -> UserEmployee:
        user = self.dao.find_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif not self._verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is incorrect")

        employee = self.dao_employee.find_by_id(user.employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data(Employee) Not Found!')
        if employee:
            if not employee.status:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Employee Is Disable')

        return UserEmployee(
            user=ModelLogin(
                id=user.id,
                username=user.username,
                description=user.description,
                employee_id=user.employee_id,
                status=user.status,
                created_at=user.created_at,
                updated_at=user.updated_at
            ),
            employee=EmployeeResponse(
                id=employee.id,
                code=employee.code,
                name=employee.name,
                surname=employee.surname,
                description=employee.description,
                building_id=employee.building_id,
                status=employee.status,
                created_at=employee.created_at,
                updated_at=employee.updated_at
            )
        )
        # history_data = UserHistoryCreate(
        #     user_id=user.id,
        #     action="LOGIN"
        # )
        # self.history_service.create_history(history_data)
        # res = UserResponse.model_validate(user)
        # return res.model_copy(
        #     update={"token": self.create_token(res.id, res)}
        # )
        # return login

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

    # @staticmethod
    # def create_token(user_id: int, user: UserResponse, token_duration=timedelta(minutes=int(TOKEN_EXPIRE_MINUTES)),
    #                  token_type="access") -> str:
    #     token_date_expires = datetime.now(timezone.utc) + token_duration
    #     token_json = {
    #         "sub": str(user_id),
    #         "type": token_type,
    #         "exp": token_date_expires,
    #         "iat": datetime.now(timezone.utc),
    #         "role": user.user_type,
    #     }
    #     return jwt.encode(token_json, SECRET_KEY, ALGORITHM)

    # def verify_token(self, token: str, expected_type: str = "access"):
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         if payload.get("type") != expected_type:
    #             raise ValueError
    #         user_id = int(str(payload.get("sub")))
    #
    #         if user_id is None:
    #             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token without user ID")
    #
    #         # user_id = int(user_id)
    #
    #     except (JWTError, TypeError, ValueError):
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired")
    #
    #     user = self.dao.find_by_id(user_id)
    #
    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token user not found")
    #     return user


# from utils.database import SessionLocal
# from building.database import models
#
# database = SessionLocal()
# try:
#     service = UserEmployeeService(database)
#     data = UserEmployeeModel(
#         username="Admin",
#         password="Informatico@12",
#         description="Test User",
#         employee_id=1,
#         # profile_id=2,
#         status=True
#     )
#     user = service.create(data)
#     print(service.get_user_login('Admin', 'Informatico@12'))
# finally:
#     database.close()
