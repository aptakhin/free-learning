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

### Linting

Linting for backend:

```bash
make lint-backend
```

Also can also use VSCode flake8 extension to see linting errors online.
