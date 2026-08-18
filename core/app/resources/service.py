
from app.resources import repository
from app.resources.exceptions import ResourceAlreadyExists
from app.resources.schemas import ResourceCreate


async def create_resource(data: ResourceCreate) -> dict:
    existing = await repository.get_by_id(data.slug)
    if existing is not None:
        raise ResourceAlreadyExists(
        f"Ресурс с идентификатором {data.slug} уже существует."
        )
        
    return await repository.create(data.model_dump())

async def list_resources() -> list[dict]:
    return await repository.list_all()