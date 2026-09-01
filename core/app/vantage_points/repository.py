from pymongo.errors import DuplicateKeyError

from app.db import vantage_points
from app.vantage_points.exceptions import VantagePointAlreadyExists


async def create(data: dict) -> dict:
    document = {
        "_id": data["slug"],
        "name": data["name"],
        "country": data["country"],
        "operator": data["operator"],
        "network_type": data["network_type"],
        "mode": data["mode"],
    }
    
    try:
        await vantage_points.insert_one(document)
    except DuplicateKeyError:
        raise VantagePointAlreadyExists(
            f"Точка наблюдения идентификатором {data['slug']} уже существует."
        )
    return document


async def list_all()-> list[dict]:
    cursor = vantage_points.find()
    return await cursor.to_list(length=None)

async def get_by_id(vantage_point_id: str) -> dict | None:
    return await vantage_points.find_one({"_id": vantage_point_id })