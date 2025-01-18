from flask import Flask
from .routes import content_bp

def create_app(config=None):
    app = Flask(__name__)
    
    if config:
        app.config.update(config)
    
    app.register_blueprint(content_bp, url_prefix='/api/content')
    
    return app
