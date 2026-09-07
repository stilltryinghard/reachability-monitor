from datetime import UTC, datetime

from app.celery_app import celery
from app.measurements import repository_sync as measurements_repo
from app.resources import repository_sync as resources_repo
from app.verdicts import repository_sync as verdicts_repo
from app.verdicts.logic import decide_verdict

EXTERNAL_VANTAGE = "pl-vps"
INTERNAL_VANTAGE = "ru-mts-home"


@celery.task(name="verdicts.evaluate")
def evaluate() -> None:
    """
    По каждоому ресурсу достать замеры, вынести вердикт, сравнить с последним и записать новый, если он отличается.
    """
    now = datetime.now(UTC)
    resources = resources_repo.list_all()
    
    for res in resources:
        if not res.get("enabled", False):
            continue
        resource_id = res["_id"]
        
        external = measurements_repo.get_latest(resource_id, EXTERNAL_VANTAGE)
        internal = measurements_repo.get_latest(resource_id, INTERNAL_VANTAGE)
        
        verdict = decide_verdict(external, internal, now)
        
        last = verdicts_repo.get_latest_verdict(resource_id, INTERNAL_VANTAGE)
        if last is not None and last["verdict"] == verdict:
            continue
        
        verdict_doc = {
            "resource_id": resource_id,
            "vantage_id": INTERNAL_VANTAGE,
            "verdict": verdict,
            "decided_at": now,
            "based_on": {
                "external_measurement_id": external["measurement_id"] if external else None,
                "internal_measurement_id": internal["measurement_id"] if internal else None,
            },
        }
        verdicts_repo.save_verdict(verdict_doc)