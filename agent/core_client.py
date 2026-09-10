import uuid
from datetime import UTC, datetime

import httpx

CORE_URL = "http://localhost:8000"
VANTAGE_ID = "ru-mts-home"


def fetch_resources() -> list[dict]:
    with httpx.Client() as client:
        response = client.get(f"{CORE_URL}/resources/active", timeout=10)
        response.raise_for_status()
        return response.json()
    
    
def build_payload(resource_id: str, outcome: dict) -> dict:
    """Собрать готовый payload-замер из результата проверки."""
    return {
        "measurement_id": str(uuid.uuid4()),
        "resource_id": resource_id,
        "vantage_id": VANTAGE_ID,
        "measured_at": datetime.now(UTC).isoformat(),
        "result": outcome["result"],
        "details": outcome["details"],
    }
    
    
def send_payload(payload: dict) -> None:
    """Отправить готовйы payload на ядро. Кидает httpx.ConnectError при обрыве."""
    with httpx.Client() as client:
        response = client.post(f"{CORE_URL}/measurements", json=payload, timeout=10)
        response.raise_for_status()