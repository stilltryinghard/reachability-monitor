from app.db import measurements


async def save(measurement: dict) -> None:
    await measurements.insert_one(measurement)