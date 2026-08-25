from app.db import measurements


def save(measurement: dict) -> None:
    measurements.insert_one(measurement)
    