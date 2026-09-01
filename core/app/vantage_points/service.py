from app.vantage_points import repository
from app.vantage_points.exceptions import VantagePointAlreadyExists
from app.vantage_points.schemas import VantagePointCreate


async def create_vantage_point(data: VantagePointCreate) -> dict:
    existing = await repository.get_by_id(data.slug)
    if existing is not None:
        raise VantagePointAlreadyExists(
            f"Точка обзора с идентификатором {data.slug} уже существует."
        )
    
    return await repository.create(data.model_dump())

async def list_vantage_points() -> list[dict]:
    return await repository.list_all()