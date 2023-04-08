"""."""

import logging.config  # noqa: WPS301

from colorama import Fore
from log import init_logger  # noqa: WPS301

from base.routes import router as base_router, auth_router
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from workdomain.routes import router as workflow_router


logger = logging.getLogger(__name__)


def create_app():
    init_logger()
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(base_router)
    app.include_router(workflow_router)

    origins = [
        'http://localhost:3000',
        'http://localhost:8000',
    ]

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        json_result = jsonable_encoder(
            {'detail': exc.errors(), 'body': exc.body}
        )
        logger.info('Request validation error: %s', json_result)
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


app = create_app()
