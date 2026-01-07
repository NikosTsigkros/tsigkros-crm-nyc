from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .api import api_bp
    from .routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    return app
