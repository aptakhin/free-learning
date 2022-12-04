install-backend:
	(cd backend && poetry install --with dev --no-root)

run:
	docker compose up --build -d

run-infra:
	docker compose up --build -d mongodb mongo-express

run-backendw:
	(cd backend && poetry run uvicorn fl_core.app:app --reload)

stop:
	docker compose stop

ps:
	docker compose ps

make test-backend:
	(cd backend && PYTHONPATH=. poetry run pytest)

make test-backendw:
	(cd backend && PYTHONPATH=. poetry run ptw)

make lint-backend:
	(cd backend && PYTHONPATH=. poetry run flake8)
