# Install
install-backend::
	(cd backend && poetry install --with dev --no-root)

install-frontend::
	(cd frontend && npm install)

# Run local with Docker
run-infra::
	docker compose --env-file backend/.env up --build -d age

stop-infra::
	docker compose stop age

run::
	docker compose --env-file backend/.env up --build -d

ps::
	docker compose ps

rerun-infra:: stop-infra run-infra

# Run with watchable fs changes
run-backendw::
	(cd backend && poetry run uvicorn app:app --reload)

run-frontendw::
	(cd frontend && npm run dev)

# Test
make test-backend::
	(cd backend && PYTHONPATH=. poetry run pytest)

make test-backendw::
	(cd backend && PYTHONPATH=. poetry run ptw . --now)

make test-acc::
	(cd acceptance && npm run test)

make test-accw::
	(cd acceptance && npm run testw)

make lint-backend::
	(cd backend && PYTHONPATH=. poetry run flake8)
