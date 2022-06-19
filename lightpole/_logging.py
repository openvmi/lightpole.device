import logging
import logging.handlers

_logger = logging.getLogger("vmilabs")

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_logger.addHandler(NullHandler())

def enableFileHandler(handler=None):
    LOG_FILENAME = "steetlight.out"
    if handler is None:
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME,
            maxBytes=50 * 1024 * 1024,
            backupCount= 10,
        )
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
        formatter = logging.Formatter(FORMAT)
        handler.setFormatter(formatter)
    _logger.addHandler(handler)

def enableConsoleHandler(handler=None):
    if handler is None:
        handler = logging.StreamHandler()
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s]: %(message)s"
        formatter = logging.Formatter(FORMAT)
        handler.setFormatter(formatter)
    _logger.addHandler(handler)

def error(msg):
    _logger.error(msg)

def warning(msg):
    _logger.warning(msg)

def debug(msg):
    _logger.debug(msg)

def info(msg):
    _logger.info(msg)

def setLogLevel(level):
    obj = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "notset": logging.NOTSET
    }
    lowcaseLevel = level.lower()
    logLevel = obj.get(lowcaseLevel, logging.WARNING)
    _logger.setLevel(logLevel)



