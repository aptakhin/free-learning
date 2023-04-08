import logging
import logging.config  # noqa: WPS301
from typing import Any

from colorama import Fore, just_fix_windows_console


class ColorfulConsoleFormatter(logging.Formatter):
    # def __init__(self) -> None:
    #     pass

    def formatException(self, ei):
        traceback = super().formatException(ei)
        return self.colorize_own_code(traceback)

    def colorize_own_code(self, code):
        lines = []
        for line in code.split('\n'):
            if 'File' in line and not 'Library/Caches' in line:
                line = Fore.LIGHTRED_EX + line + Fore.RESET
            lines.append(line)
        return '\n'.join(lines)


class FigureLogRecord(logging.LogRecord):
    def getMessage(self) -> str:  # noqa: N802
        msg = str(self.msg)
        if self.args:
            msg = msg.format(*self.args)
        return msg


def make_log_record_factory(*args, **kwargs):
    module_name = args[0]
    # Fallback to old logging style
    if module_name.startswith('uvicorn') or module_name in ('_client', 'httpx._client', 'asyncio'):
        return logging.LogRecord(*args, **kwargs)

    return FigureLogRecord(*args, **kwargs)


def listloggers():
    rootlogger = logging.getLogger()
    print(rootlogger)
    for log_handler in rootlogger.handlers:
        print('     %s' % log_handler)  # noqa: WPS323, WPS421

    for name, logger in logging.Logger.manager.loggerDict.items():
        print('+ [%-40s] %s ' % (name, logger))  # noqa: WPS323, WPS421
        if not isinstance(logger, logging.PlaceHolder):
            for log_handler in logger.handlers:
                print('     %s' % log_handler)  # noqa: WPS323, WPS421


def init_logger():
    # override uvicorn
    parent = logging.getLogger('uvicorn')
    for log_handler in parent.handlers:
        parent.removeHandler(log_handler)

    parent = logging.getLogger('uvicorn.access')
    for log_handler in parent.handlers:
        parent.removeHandler(log_handler)

    config = _make_base_config_dict()
    logging.config.dictConfig(config)
    logging.setLogRecordFactory(make_log_record_factory)

    just_fix_windows_console()


def _make_base_config_dict() -> dict[str, Any]:
    base_dict_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console_formatter',
                'level': 'NOTSET',
                'stream': 'ext://sys.stdout',
            },
            'console_fallback_formatter': {
                'class': 'logging.StreamHandler',
                'formatter': 'console_formatter',
                'level': 'NOTSET',
                'stream': 'ext://sys.stdout',
            },
        },
        'formatters': {
            'default': {
                'format': '{asctime} {levelname:8s} {name:15s} {message}',
                'datefmt': '%Y-%m-%d %H:%M:%S',  # noqa: WPS323
                'style': '{',
            },
            'console_formatter': {
                '()': 'log.ColorfulConsoleFormatter',
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
            'app': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'base': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'log': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            # misc
            'uvicorn': {
                'handlers': ['console_fallback_formatter'],
                'level': 'INFO',
            },
            'uvicorn.access': {
                'handlers': ['console_fallback_formatter'],
                'level': 'INFO',
            },
            'ddtrace': {
                'handlers': ['console_fallback_formatter'],
                'level': 'INFO',
            },
            'sqlalchemy.engine': {
                'handlers': ['console'],
                'level': 'ERROR',
            },
        },
    }
    return base_dict_config
