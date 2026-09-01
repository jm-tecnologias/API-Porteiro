from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from utils.base import Base

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
# from utils.buildingSchema.building_schema import BuildingSchema
# from utils.buildingSchema.building_schema import AddressSchema
# from utils.buildingSchema.building_schema import ContactSchema
# from utils.authSchema.profileSchema.user_profile_schema import ProfileSchema
# from utils.RHSchema.department_schema import DepartmentSchema
# from utils.RHSchema.employee_schema import EmployeeSchema
# from utils.RHSchema.depart_employee_schema import DepartmentEmployeeSchema
# from utils.authSchema.authemployee.user_schema import EmployeeUserSchema
# from utils.APSchema.apartment_schema import ApartmentSchema
# from utils.APSchema.client_schema import ClientSchema
# from utils.APSchema.member_schema import MemberSchema
# from utils.APSchema.checkIn_checkOut import CheckInOutSchema
# from utils.authSchema.authclient.user_schema import MemberUserSchema
# from utils.APSchema.historic_schema import HistoricSchema
# from utils.APSchema.visitor_schema import VisitorSchema
# from utils.APSchema.visitor_check_in_out import VisitorCheckInOutSchema


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
    from utils.schemas.building_schema import BuildingSchema
    from utils.schemas.building_schema import AddressSchema
    from utils.schemas.building_schema import ContactSchema
    from utils.schemas.user_profile_schema import ProfileSchema
    from utils.schemas.depart_employee_schema import DepartmentEmployeeSchema
    from utils.schemas.employee_user_schema import EmployeeUserSchema
    from utils.schemas.client_user_schema import MemberUserSchema
    from utils.schemas.historic_schema import HistoricSchema
    from utils.schemas.visitor_schema import VisitorSchema
    from utils.schemas.visitor_check_in_out import VisitorCheckInOutSchema

    print("Tabelas registadas:", list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)
    print("Base de dados criada com sucesso.")
    # print(f"Localização: {DATABASE_FILE}")
