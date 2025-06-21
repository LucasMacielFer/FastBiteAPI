from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app