import uuid
from datetime import UTC, datetime

import httpx

CORE_URL = "http://localhost:8000"
VANTAGE_ID = "ru-mts-home"


def send_measurement(resource_id: str, outcome: dict) -> None:
    payload = {
        "measurement_id": str(uuid.uuid4()),
        "resource_id": resource_id, 
        "vantage_id": VANTAGE_ID,
        "measured_at": datetime.now(UTC).isoformat(),
        "result": outcome["result"],
        "details": outcome["details"],
    }
    with httpx.Client() as client:
        response = client.post(f"{CORE_URL}/measurements", json=payload, timeout=10)
        response.raise_for_status()