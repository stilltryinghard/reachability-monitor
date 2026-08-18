from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.db_name]


#Хэндлеры на коллекции. Сами коллекции создаются автоматически при первом обращении к ним.
vantage_points = db["vantage_points"]
resources = db["resources"]
measurements = db["measurements"]
verdicts = db["verdicts"]
