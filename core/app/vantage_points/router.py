from fastapi import APIRouter, HTTPException, status

from app.vantage_points import service
from app.vantage_points.exceptions import VantagePointAlreadyExists
from app.vantage_points.schemas import VantagePointCreate, VantagePointOut

router = APIRouter(prefix="/vantage-points", tags=["vantage-points"])


@router.post("", response_model=VantagePointOut, status_code=status.HTTP_201_CREATED)
async def create_vantage_point(data: VantagePointCreate):
    try:
        created = await service.create_vantage_point(data)
    except VantagePointAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return created


@router.get("", response_model=list[VantagePointOut])
async def list_vantage_points():
    return await service.list_vantage_points()
