from datetime import UTC, datetime

from app.measurements import repository
from app.measurements.schemas import MeasurementCreate


async def accept_measurement(data: MeasurementCreate) -> None:
    existing = await repository.get_measurement_by_id(data.measurement_id)
    if existing is not None:
        return
    
    document = data.model_dump()
    document["result"] = data.result.value
    document["received_at"] = datetime.now(UTC)
    await repository.save(document)
    