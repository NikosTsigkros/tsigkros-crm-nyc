from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user

from app.constants import CUSTOMER_CATEGORIES, ROLE_ADMIN, ROLE_EMPLOYEE, ROLE_OPTIONS
from app.models import Customer, User
from app.utils import role_required

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
@login_required
def index():
    return render_template("index.html")

@web_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web.login"))

@web_bp.route("/customers")
@login_required
def customers():
    query = Customer.query
    if current_user.role == ROLE_EMPLOYEE:
        query = query.filter_by(created_by_id=current_user.id)
    customers_list = query.order_by(Customer.created_at.desc()).all()
    return render_template(
        "customers.html",
        customers=customers_list,
        categories=CUSTOMER_CATEGORIES,
    )

@web_bp.route("/admin/users")
@login_required
@role_required(ROLE_ADMIN)
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users, roles=ROLE_OPTIONS)