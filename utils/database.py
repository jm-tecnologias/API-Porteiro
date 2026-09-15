from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from building.database.base import Base

PROJECT_ROOT = Path(__file__).parent.parent

DATABASE_DIR = PROJECT_ROOT


DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FLE = DATABASE_DIR / "building.db"

DATABASE_URL = f"sqlite:///{DATABASE_FLE.as_posix()}"


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Schemas do Banco de dados
from building.database.schemas.building_schema import BuildingSchema, ContactSchema, AddressSchema
from building.database.schemas.client_schema import ClientSchema
from building.database.schemas.member_schema import  MemberSchema
from building.database.schemas.building_schema import BuildingSchema, ContactSchema, AddressSchema
from building.database.schemas.member_check_in_out_schema import MemberCheckInOutSchema
from building.database.schemas.apartment_schema import ApartmentSchema
from building.database.schemas.depart_employee_schema import DepartmentEmployeeSchema
from building.database.schemas.department_schema import DepartmentSchema
from building.database.schemas.employee_schema import EmployeeSchema
from building.database.schemas.employee_user_schema import EmployeeUserSchema
#, UserHistorySchema
from building.database.schemas.historic_schema import HistoricSchema
from building.database.schemas.profile_schema import ProfileSchema
from building.database.schemas.visitor_schema import VisitorSchema
from building.database.schemas.visitor_check_in_out_schema import VisitorCheckInOutSchema
from building.database.schemas.employee_user_profile_schema import UserProfileEmployeeSchema
from building.database.schemas.permission_schema import PermissionSchema
from building.database.schemas.profile_permission_schema import ProfilePermissionSchema
from building.database.schemas.member_user_schema import MemberUserSchema


def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def create_database_tables() -> None:
    """
    Importa os modelos e cria as tabelas registadas.
    """
    from building.database.schemas.building_schema import BuildingSchema, ContactSchema, AddressSchema
    from building.database.schemas.client_schema import ClientSchema
    from building.database.schemas.member_schema import MemberSchema
    from building.database.schemas.member_check_in_out_schema import MemberCheckInOutSchema
    from building.database.schemas.building_schema import BuildingSchema, ContactSchema, AddressSchema
    from building.database.schemas.apartment_schema import ApartmentSchema
    from building.database.schemas.depart_employee_schema import DepartmentEmployeeSchema
    from building.database.schemas.department_schema import DepartmentSchema
    from building.database.schemas.employee_schema import EmployeeSchema
    from building.database.schemas.employee_user_schema import EmployeeUserSchema
    # , UserHistorySchema
    from building.database.schemas.historic_schema import HistoricSchema
    from building.database.schemas.profile_schema import ProfileSchema
    from building.database.schemas.visitor_schema import VisitorSchema
    from building.database.schemas.visitor_check_in_out_schema import VisitorCheckInOutSchema
    from building.database.schemas.employee_user_profile_schema import UserProfileEmployeeSchema
    from building.database.schemas.permission_schema import PermissionSchema
    from building.database.schemas.profile_permission_schema import ProfilePermissionSchema
    from building.database.schemas.ordinary_visitor_schema import OrdinaryVisitorSchema
    from building.database.schemas.member_user_schema import MemberUserSchema

    print("Tabelas registadas:", list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)
    print("Base de dados criada com sucesso.")
    # print(f"Localização: {DATABASE_FILE}")
