import uuid
from datetime import UTC, datetime

from app.celery_app import celery
from app.measurements import repository_sync as measurements_repo
from app.probing.checker import check_resource
from app.resources import repository_sync as resources_repo

VANTAGE_ID = "pl-vps"   # внешний пробник = польская нода


@celery.task(name="probing.probe_resource")
def probe_resource(resource_id: str, url: str) -> None:
    outcome = check_resource(url)

    now = datetime.now(UTC)
    measurement = {
        "measurement_id": str(uuid.uuid4()),
        "resource_id": resource_id,
        "vantage_id": VANTAGE_ID,
        "measured_at": now,
        "received_at": now,
        "result": outcome["result"],
        "details": outcome["details"],
    }

    measurements_repo.save(measurement)


@celery.task(name="probing.dispatch")
def dispatch() -> None:
    resources = resources_repo.list_all()
    for res in resources:
        if not res.get("enabled", False):
            continue
        probe_resource.delay(res["_id"], res["url"])