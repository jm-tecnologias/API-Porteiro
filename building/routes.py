from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from building.model import BuildingModel, BuildingResponse
from building.service import BuildingService
from utils.database import get_database

building_router = APIRouter(prefix='/building', tags=['Buildings'])


def get_build_service(database: Session = Depends(get_database)) -> BuildingService:
    return BuildingService(database)


@building_router.post('/register', response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
async def create(build: BuildingModel, service: BuildingService = Depends(get_build_service)) -> BuildingResponse:
    return service.create(build)


@building_router.patch('/update/{build_id}', response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
async def update(build_id: int, build: BuildingModel,
                 service: BuildingService = Depends(get_build_service)) -> BuildingResponse:
    return service.update(build_id=build_id, build_data=build)


@building_router.get('/list-all/{status}', response_model=list[BuildingResponse], status_code=status.HTTP_200_OK)
async def get_buildings(status: bool, service: BuildingService = Depends(get_build_service)) -> list[BuildingResponse]:
    return service.find_all_buildings(status=status)
