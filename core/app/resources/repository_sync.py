from app.db_sync import resources


def list_all() -> list[dict]:
    return list(resources.find())
