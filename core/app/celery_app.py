from celery import Celery

from app.config import settings

celery = Celery(
    "reachability",
    broker=settings.rabbitmq_url,
    backend=None, #Результаты задач не сохраняются, воркер пишет сразу в Монго.
)

celery.conf.timezone = "UTC"

celery.autodiscover_tasks(["app.probing", "app.measurements", "app.verdicts"])

celery.conf.beat_schedule = {
    "dispatch-probes": {
        "task": "probing.dispatch",
        "schedule": 30.0,
    },
    "evaluate-verdicts": {
        "task": "verdicts.evaluate",
        "schedule":  30.0,
    },
}