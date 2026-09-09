from pymongo.errors import DuplicateKeyError

from app.db import resources
from app.resources.exceptions import ResourceAlreadyExists


async def create(data: dict) -> dict:
    document = {
        "_id": data["slug"],
        "name": data["name"],
        "url": data["url"],
        "check_interval_sec": data["check_interval_sec"],
        "enabled": True,
    }
    
    try:
        await resources.insert_one(document)
    except DuplicateKeyError:
        raise ResourceAlreadyExists(
            f"Ресурс с идентификатором {data['slug']} уже существует."
        )
    return document

    
    
async def list_all()-> list[dict]:
    cursor = resources.find()
    return await cursor.to_list(length=None)
    

async def get_by_id(resource_id: str) -> dict | None:
    return await resources.find_one({"_id": resource_id})


async def list_active() -> list[dict]:
    cursor = resources.find({"enabled": True})
    return await cursor.to_list(length=None)