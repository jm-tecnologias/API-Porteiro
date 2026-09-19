from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from building.address.routes import address_router
from building.apartment.routes import apartment_router
from building.auth.user.client.routes import client_user_router
from building.auth.user.employee.routes import employee_user_router
from building.client.member.routes import member_router
from building.client.routes import client_router
from building.contact.routes import contact_router
from building.occupational_historic.routes import historic_router
from building.rh.department.routes import department_router
from building.rh.department_employee.routes import depemp_router
from building.rh.employee.routes import employee_router
from building.routes import building_router
from utils.database import create_database_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_tables()
    yield


app = FastAPI(title="Building-Management", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Hello": "World"}


app.include_router(building_router)
app.include_router(contact_router)
app.include_router(address_router)
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(depemp_router)
app.include_router(apartment_router)
app.include_router(employee_user_router)
app.include_router(client_user_router)
app.include_router(client_router)
app.include_router(historic_router)
app.include_router(member_router)
