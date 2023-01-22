# Hello

All instructions are below. And feel free to look into `Makefile` for the full reference.

## Run service

Run all with Docker to look at service "as is":

```bash
make run
```

### Run for dev

Install:

```bash
make install-backend
make install-frontend
```

Run for dev with watchable things:

```bash
make run-infra
make run-backendw
```

In separate shell can run watched:

```bash
make run-frontendw
```

### Testing

Run watchable backend testing `pytest-watcher` (Separate shell & requires `make run-infra` earlier):

```bash
make test-backendw
```

### DB migrations

Alembic powered on SQL-part of `Apache Age`.

```bash
cd backend
poetry run alembic revision --autogenerate -m '...'
poetry run alembic upgrade head
```

### Linting

Linting for backend:

```bash
make lint-backend
```

Also can also use VSCode flake8 extension to see linting errors online.

### Build

```bash
# frontend
cd frontend
npm run buildAndExport
# output will in /frontend/out

python -m http.server --directory out 3000
```

```bash
# backend
docker build -t registry.digitalocean.com/frlr/backend:003 backend
docker push registry.digitalocean.com/frlr/backend:003

# frontend
docker build -t registry.digitalocean.com/frlr/frontend:003 frontend
docker push registry.digitalocean.com/frlr/frontend:003

# age
docker pull apache/age:v1.1.0
docker tag apache/age:v1.1.0 registry.digitalocean.com/frlr/age:v1.1.0
docker push registry.digitalocean.com/frlr/age:v1.1.0
```

Helm:

```bash
cd infra
kubectl apply -f ingress.yaml

helm upgrade --install backend backend-helm/ -f prod/backend.values.yaml
helm upgrade --install frontend backend-helm/ -f prod/frontend.values.yaml
helm upgrade --install age age-helm/ -f prod/age.values.yaml
helm upgrade --install ingress ingress-helm/ -f prod/ingress.values.yaml
helm upgrade --install nginx-controller/ nginx-stable/nginx-ingress
helm upgrade --install datadog -f prod/datadog.values.yaml --set datadog.site='datadoghq.eu' --set datadog.apiKey='...' datadog/datadog
```

DigitalOcean and pvc: https://docs.digitalocean.com/products/kubernetes/how-to/add-volumes/
