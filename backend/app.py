"""."""

import logging.config  # noqa: WPS301

from base.routes import router as base_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from workdomain.routes import router as workflow_router


logger = logging.getLogger(__name__)


base_logger_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
        },
    },
    'formatters': {
        'default': {
            'format': '{asctime} {levelname:8s} {name:15s} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',  # noqa: WPS323
            'style': '{',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'sqlalchemy.engine': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}


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
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.get('/api/v1/healthz')
    async def healthz():  # noqa: WPS430
        """."""
        return {'status': True}

    logging.config.dictConfig(base_logger_config)
    logger.info('Started')
    return app


app = create_app()
