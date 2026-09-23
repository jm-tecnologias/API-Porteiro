from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from building.model import BuildingModel, BuildingResponse, BuildingResponseMoreDetails
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


@building_router.get('/list-all', response_model=list[BuildingResponse], status_code=status.HTTP_200_OK)
async def list_buildings(service: BuildingService = Depends(get_build_service)) -> list[BuildingResponse]:
    return service.find_all_buildings()


@building_router.get('/get/{building_id}', response_model=BuildingResponseMoreDetails, status_code=status.HTTP_200_OK)
async def get(building_id: int, service: BuildingService = Depends(get_build_service)) -> BuildingResponseMoreDetails:
    return service.get_building(building_id)
