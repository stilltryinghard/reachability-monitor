from app.db_sync import measurements


def save(measurement: dict) -> None:
    measurements.insert_one(measurement)


def get_latest(resource_id: str, vantage_id: str) -> dict | None:
    return measurements.find_one(
        {"resource_id": resource_id, "vantage_id": vantage_id},
        sort=[("measured_at", -1)],
    )
