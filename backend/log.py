import logging
import logging.config
from colorama import Fore

from typing import Any


class ColorfulConsoleFormatter(logging.Formatter):
    # def __init__(self) -> None:
    #     pass

    def formatException(self, ei):
        traceback = super().formatException(ei)
        return self.colorize_own_code(traceback)
        # return '{}{}{}'.format(Fore.LIGHTRED_EX, self.colorize_own_code(traceback), Fore.RESET)

    def colorize_own_code(self, code):
        lines = []
        for line in code.split('\n'):
            if 'File' in line and not 'Library/Caches' in line:
                line = Fore.LIGHTRED_EX + line + Fore.RESET
            lines.append(line)
        return '\n'.join(lines)



class FigureLogRecord(logging.LogRecord):
    def getMessage(self) -> str:
        msg = str(self.msg)
        if self.args:
            msg = msg.format(*self.args)
        return msg

def make_log_record_factory(*args, **kwargs):
    module_name = args[0]
    # Fallback to old logging style
    if module_name.startswith('uvicorn'):
        return logging.LogRecord(*args, **kwargs)

    return FigureLogRecord(*args, **kwargs)


def listloggers():
    rootlogger = logging.getLogger()
    print(rootlogger)
    for handler in rootlogger.handlers:
        print('     %s' % handler)

    for name, logger in logging.Logger.manager.loggerDict.items():
        print('+ [%-40s] %s ' % (name, logger))
        if not isinstance(logger, logging.PlaceHolder):
            for handler in logger.handlers:
                print('     %s' % handler)


def init_logger():
    # override uvicorn
    parent = logging.getLogger('uvicorn')
    for x in parent.handlers:
        parent.removeHandler(x)

    parent = logging.getLogger('uvicorn.access')
    for x in parent.handlers:
        parent.removeHandler(x)

    config = _make_base_config_dict()
    logging.config.dictConfig(config)
    logging.setLogRecordFactory(make_log_record_factory)

    from colorama import just_fix_windows_console
    just_fix_windows_console()

    # listloggers()

# + [concurrent.futures                      ] <Logger concurrent.futures (DEBUG)>
# + [concurrent                              ] <logging.PlaceHolder object at 0x1009a9ba0>
# + [asyncio                                 ] <Logger asyncio (DEBUG)>
# + [uvicorn.error                           ] <Logger uvicorn.error (INFO)>
# + [uvicorn                                 ] <Logger uvicorn (INFO)>
#      <StreamHandler <stderr> (NOTSET)>
# + [uvicorn.access                          ] <Logger uvicorn.access (INFO)>
#      <StreamHandler <stdout> (NOTSET)>

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

            'sqlalchemy.engine': {
                'handlers': ['console'],
                'level': 'ERROR',
            },
        },
    }
    return base_dict_config
