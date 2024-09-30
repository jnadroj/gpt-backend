from flask import Flask
from flask_cors import CORS
from app.routes import init_routes
from app.config.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_routes(app)
    return app
