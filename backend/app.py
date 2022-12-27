"""."""

from base.routes import router as base_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from workdomain.routes import router as workflow_router


def create_app():
    app = FastAPI()
    app.include_router(base_router)
    app.include_router(workflow_router)

    origins = [
        'http://localhost:3000',
        'http://localhost:8000',
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get('/api/v1/healthz')
    async def healthz():
        """."""
        return {'status': True}

    return app

app = create_app()
