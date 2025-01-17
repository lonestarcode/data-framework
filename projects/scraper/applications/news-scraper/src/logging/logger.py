import logging
import logging.config
from functools import wraps
from time import time
from .config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name):
    return logging.getLogger(name)

def log_execution_time(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            try:
                result = func(*args, **kwargs)
                execution_time = time() - start_time
                logger.debug(
                    f"Function {func.__name__} executed in {execution_time:.2f}s",
                    extra={
                        "function": func.__name__,
                        "execution_time": execution_time
                    }
                )
                return result
            except Exception as e:
                execution_time = time() - start_time
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra={
                        "function": func.__name__,
                        "execution_time": execution_time,
                        "error": str(e)
                    },
                    exc_info=True
                )
                raise
        return wrapper
    return decorator 