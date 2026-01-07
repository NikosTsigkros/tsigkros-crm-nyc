from flask import Flask

ROLE_EMPLOYEE = "employee"
ROLE_MANAGER = "manager"
ROLE_ADMIN = "admin"
ROLE_OPTIONS = [ROLE_EMPLOYEE, ROLE_MANAGER, ROLE_ADMIN]
CUSTOMER_CATEGORIES = ["Lead", "Active", "Inactive", "Cancelled"]

def create_app() -> Flask:
    app = Flask(__name__)

    from .api import api_bp
    from .routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    return app
