from fastapi import APIRouter, HTTPException, status

from app.resources import service
from app.resources.exceptions import ResourceAlreadyExists
from app.resources.schemas import ResourceCreate, ResourceOut

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", response_model=ResourceOut, status_code=status.HTTP_201_CREATED)
async def create_resource(data: ResourceCreate):
    try:
        created = await service.create_resource(data)
    except ResourceAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return created


@router.get("", response_model=list[ResourceOut])
async def list_resources():
    return await service.list_resources()