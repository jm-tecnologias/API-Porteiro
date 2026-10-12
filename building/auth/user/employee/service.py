from building.database.schemas.employee_user_schema import UserEmployeeSchema
from building.rh.employee.dao import EmployeeDAO
from building.auth.user.employee.dao import UserEmployeeDAO
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from building.auth.user.employee.model import UserEmployeeResponse, UserEmployeeModel, ModelLogin, UserEmployee, \
    LoginTokenResponse
from building.rh.employee.model import EmployeeResponse
from utils.auth_service import AuthService


class UserEmployeeService:
    def __init__(self, database: Session):
        self.dao = UserEmployeeDAO(database)
        self.dao_employee = EmployeeDAO(database)
        self.auth_helper = AuthService(database=database, dao_class=UserEmployeeDAO)
        # self.dao_profile = ProfileDAO(database)

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
            password=self.auth_helper.hash_password(user_data.password),
            # profile_id=user_data.profile_id,
            username=user_data.username
        )
        return self.dao.create(new)

    def get_user_login(self, username: str, password: str) -> LoginTokenResponse:
        user = self.dao.find_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        elif not self.auth_helper.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Password is incorrect")

        employee = self.dao_employee.find_by_id(user.employee_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Parent Data(Employee) Not Found!')
        if employee:
            if not employee.status:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Employee Is Disable')
        access_token = self.auth_helper.create_token(user.id)

        return LoginTokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserEmployee(
                userModel=ModelLogin(
                    id=user.id,
                    username=user.username,
                    description=user.description,
                    employee_id=user.employee_id,
                    status=user.status,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ),
                employeeModel=EmployeeResponse(
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
        )



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
