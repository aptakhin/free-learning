"""."""
from fastapi import FastAPI
from base.routes import router as base_router
from workflow.routes import router as workflow_router


def create_app():
    app = FastAPI()
    app.include_router(base_router)
    app.include_router(workflow_router)

    @app.get('/api/v1/healthz')
    async def healthz():
        """."""
        return {'status': True}

    return app

app = create_app()
