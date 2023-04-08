import logging.config

from base.config import Settings
from base.db import create_db_sync
from base.db_age import Database  # noqa: WPS301
from base.routes import auth_router
from base.routes import router as base_router
from colorama import Fore
from container import container
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from log import init_logger  # noqa: WPS301
from workdomain.routes import router as workflow_router

logger = logging.getLogger(__name__)


def create_app():
    init_logger()
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(base_router)
    app.include_router(workflow_router)

    settings = Settings()
    container.register(Settings, instance=settings)
    database = create_db_sync(settings)
    container.register(Database, instance=database)

    origins = [
        'http://localhost:3000',
        'http://localhost:8000',
    ]

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError,
    ):
        json_result = jsonable_encoder(
            {'detail': exc.errors(), 'body': exc.body},
        )
        logger.info('Request validation error: {}', json_result)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=json_result,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.get('/api/v1/healthz')
    async def healthz():  # noqa: WPS430
        """."""
        return {'status': True}

    logger.info('Started {0}{1}{2}', Fore.LIGHTRED_EX, 'instance', Fore.RESET)
    return app


container.register(FastAPI, create_app)
