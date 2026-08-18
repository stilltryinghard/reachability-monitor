from fastapi import FastAPI

from app.db import client
from app.resources.router import router as resources_router

app = FastAPI(title="Reachability Monitor")

app.include_router(resources_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    #ping - самая дешевая команда для проверки доступности базы данных. Она не требует аутентификации и не создает нагрузку на базу данных.
    await client.admin.command("ping")
    return {"db": "ok"}

