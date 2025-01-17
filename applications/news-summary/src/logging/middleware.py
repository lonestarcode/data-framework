from flask import request, g
import time
from .logger import get_logger

logger = get_logger('api')

class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO')
        method = environ.get('REQUEST_METHOD')
        
        # Start timer
        start_time = time.time()
        
        def custom_start_response(status, headers, exc_info=None):
            # Log request completion
            duration = time.time() - start_time
            status_code = int(status.split()[0])
            
            log_data = {
                'path': path,
                'method': method,
                'status_code': status_code,
                'duration': f"{duration:.2f}s"
            }
            
            if status_code >= 400:
                logger.error('Request failed', extra=log_data)
            else:
                logger.info('Request completed', extra=log_data)
                
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response) 