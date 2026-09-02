from app.db import measurements


async def save(measurement: dict) -> None:
    await measurements.insert_one(measurement)
    
    
async def get_measurement_by_id(measurement_id: str) -> dict | None:
    return await measurements.find_one({"measurement_id": measurement_id})