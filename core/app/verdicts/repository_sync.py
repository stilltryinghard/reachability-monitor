from app.db_sync import verdicts


def save_verdict(verdict: dict) -> None:
    verdicts.insert_one(verdict)


def get_latest_verdict(resource_id: str, vantage_id: str) -> dict | None:
    return verdicts.find_one(
        {"resource_id": resource_id, "vantage_id": vantage_id},
        sort=[("decided_at", -1)],
    )
