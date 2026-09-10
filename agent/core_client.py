import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

import httpx

RESOURCES_CACHE = Path("resources_cache.json")

CORE_URL = "http://localhost:8000"
VANTAGE_ID = "ru-mts-home"


def _save_cache(resources: list[dict]) -> None:
    with open(RESOURCES_CACHE, "w") as f:
        json.dump(resources, f)
        

def _load_cache() -> list[dict]:
    if not RESOURCES_CACHE.exists():
        return []
    with open(RESOURCES_CACHE, "r") as f:
        return json.load(f)
    

def fetch_resources() -> list[dict]:
    try:
        with httpx.Client() as client:
            response = client.get(f"{CORE_URL}/resources/active", timeout=10)
            response.raise_for_status()
            resources = response.json()
        _save_cache(resources)
        return resources
    except httpx.ConnectError:
        return _load_cache()
            
    
    
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