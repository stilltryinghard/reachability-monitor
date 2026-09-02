from fastapi import APIRouter, status

from app.measurements import service
from app.measurements.schemas import MeasurementCreate

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def accept_measurement(data: MeasurementCreate):
    await service.accept_measurement(data)
    return {"status": "accepted"}
