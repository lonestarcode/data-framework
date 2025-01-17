from typing import Dict, Optional, Callable
from functools import wraps
import time
from src.logging.logger import get_logger
from src.monitoring.metrics import SCRAPE_FAILURES, PROCESSING_ERRORS
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError
from openai.error import OpenAIError
from anthropic import AnthropicError

logger = get_logger('error_handler')

class ScraperError(Exception):
    def __init__(self, message: str, error_type: str, is_recoverable: bool = True):
        self.message = message
        self.error_type = error_type
        self.is_recoverable = is_recoverable
        super().__init__(self.message)

class ErrorHandler:
    def __init__(self, max_retries: int = 3, base_delay: int = 5):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def handle_error(self, error: Exception, context: Dict) -> Dict:
        """
        Handle different types of errors and determine recovery strategy
        """
        if isinstance(error, RequestException):
            return self._handle_network_error(error, context)
        elif isinstance(error, SQLAlchemyError):
            return self._handle_database_error(error, context)
        elif isinstance(error, (OpenAIError, AnthropicError)):
            return self._handle_llm_error(error, context)
        else:
            return self._handle_generic_error(error, context)

    def _handle_network_error(self, error: RequestException, context: Dict) -> Dict:
        SCRAPE_FAILURES.inc()
        
        if error.response is not None:
            status_code = error.response.status_code
            
            if status_code == 429:  # Rate limit
                return {
                    "action": "retry",
                    "delay": int(error.response.headers.get('Retry-After', self.base_delay)),
                    "error_type": "rate_limit"
                }
            elif status_code == 404:  # Not found
                return {
                    "action": "skip",
                    "error_type": "not_found"
                }
            elif status_code >= 500:  # Server error
                return {
                    "action": "retry",
                    "delay": self.base_delay,
                    "error_type": "server_error"
                }
        
        return {
            "action": "retry",
            "delay": self.base_delay,
            "error_type": "network_error"
        }

    def _handle_database_error(self, error: SQLAlchemyError, context: Dict) -> Dict:
        PROCESSING_ERRORS.inc()
        
        if "deadlock" in str(error).lower():
            return {
                "action": "retry",
                "delay": self.base_delay,
                "error_type": "deadlock"
            }
        
        return {
            "action": "alert",
            "error_type": "database_error",
            "is_critical": True
        }

    def _handle_llm_error(self, error: Exception, context: Dict) -> Dict:
        PROCESSING_ERRORS.inc()
        
        if "rate_limit" in str(error).lower():
            return {
                "action": "retry",
                "delay": 60,  # Longer delay for LLM rate limits
                "error_type": "llm_rate_limit"
            }
        
        return {
            "action": "fallback",
            "error_type": "llm_error",
            "fallback": "basic_summarizer"
        }

    def _handle_generic_error(self, error: Exception, context: Dict) -> Dict:
        PROCESSING_ERRORS.inc()
        return {
            "action": "alert",
            "error_type": "unknown",
            "is_critical": False
        }

def with_error_handling(max_retries: int = 3, base_delay: int = 5):
    """
    Decorator for functions that need error handling and recovery
    """
    error_handler = ErrorHandler(max_retries=max_retries, base_delay=base_delay)

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    context = {
                        "function": func.__name__,
                        "args": args,
                        "kwargs": kwargs,
                        "attempt": retries + 1
                    }
                    
                    error_response = error_handler.handle_error(e, context)
                    logger.error(
                        f"Error in {func.__name__}: {str(e)}",
                        extra={
                            "error_type": error_response["error_type"],
                            "context": context
                        }
                    )

                    if error_response["action"] == "skip":
                        logger.info(f"Skipping operation due to {error_response['error_type']}")
                        return None
                    elif error_response["action"] == "alert":
                        if error_response.get("is_critical", False):
                            logger.critical(f"Critical error: {str(e)}")
                            raise
                        break
                    elif error_response["action"] == "fallback":
                        logger.info(f"Using fallback method: {error_response['fallback']}")
                        return handle_fallback(error_response['fallback'], *args, **kwargs)
                    elif error_response["action"] == "retry":
                        if retries < max_retries:
                            delay = error_response.get("delay", base_delay)
                            logger.info(f"Retrying in {delay} seconds...")
                            time.sleep(delay)
                            retries += 1
                            continue
                
                raise ScraperError(
                    f"Max retries ({max_retries}) exceeded",
                    error_type=error_response["error_type"]
                )
                
        return wrapper
    return decorator 