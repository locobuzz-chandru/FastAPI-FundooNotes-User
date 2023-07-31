SHELL:=/bin/bash

init:
	@pip-compile && pip-sync
migrate:
	@alembic upgrade head
drop:
	@alembic downgrade -1
run:
	@uvicorn main:api --port 8000 --reload
celery:
	@celery -A celery_app.celeryApp worker -l info --pool=solo
