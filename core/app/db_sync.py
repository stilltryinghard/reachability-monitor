from pymongo import MongoClient

from app.config import settings

sync_client: MongoClient = MongoClient(settings.mongo_url)
sync_db = sync_client[settings.db_name]

#Синхронные хендлы коллекций - для Celery-задач
resources = sync_db["resources"]
measurements = sync_db["measurements"]
verdicts = sync_db["verdicts"]
vantage_points = sync_db["vantage_points"]