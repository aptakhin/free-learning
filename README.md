# Hello

## Backend

Install

```bash
(cd backend && poetry install --with dev --no-root)
```

Running:

```bash
make run-infra
make run-backendw
```

Run all in docker compose:

```bash
make run
```

Run pytest-watch:

```bash
make test-backendw
```

Linting (and can also use VSCode flake8 extension from environment setting):
