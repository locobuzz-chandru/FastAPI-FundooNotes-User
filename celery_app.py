from os import getenv

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
celeryApp = Celery(
    __name__,
    broker=str(getenv("REDIS_URL")),
    backend=str(getenv("REDIS_URL")),
)

celeryApp.conf["broker_connection_retry_on_startup"] = True

celeryApp.autodiscover_tasks(["app.tasks"], force=True)
