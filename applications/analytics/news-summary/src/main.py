from flask import Flask
from src.logging.logger import get_logger
from src.logging.middleware import LoggingMiddleware
from src.api.auth_routes import auth_bp
from prometheus_client import start_http_server
import os

# Initialize main logger
logger = get_logger('app')

def create_app():
    app = Flask(__name__)
    
    # Initialize logging middleware
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(summary_bp, url_prefix='/api')
    app.register_blueprint(source_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    
    # Start Prometheus metrics server
    start_http_server(8000)
    
    logger.info("Application initialized successfully")
    return app

def main():
    try:
        app = create_app()
        port = int(os.getenv('PORT', 5000))
        
        logger.info(f"Starting application on port {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main() 