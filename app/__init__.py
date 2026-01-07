from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ROLE_EMPLOYEE = "employee"
ROLE_MANAGER = "manager"
ROLE_ADMIN = "admin"
ROLE_OPTIONS = [ROLE_EMPLOYEE, ROLE_MANAGER, ROLE_ADMIN]
CUSTOMER_CATEGORIES = ["Lead", "Active", "Inactive", "Cancelled"]

def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///crm.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .api import api_bp
    from .routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    return app
