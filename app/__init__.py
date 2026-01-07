from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "crm.login"

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
    login_manager.init_app(app)

    from . import models
    from .api import api_bp
    from .routes import web_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
        _seed_admin_user()
    return app

def _seed_admin_user():
    from .models import User

    if User.query.first():
        return
    username = os.getenv("CRM_ADMIN_USERNAME", "admin")
    password = os.getenv("CRM_ADMIN_PASSWORD", "admin123")
    admin = User(
        username=username,
        role=ROLE_ADMIN,
        active=True,
        password_hash=generate_password_hash(password),
    )
    db.session.add(admin)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return User.query.get(int(user_id))
