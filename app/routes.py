from os import abort
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from app.constants import (
    CUSTOMER_CATEGORIES,
    ROLE_ADMIN,
    ROLE_EMPLOYEE,
    ROLE_MANAGER,
    ROLE_OPTIONS,
)
from app.models import Customer, Interaction, User
from app.utils import _ensure_customer_access, role_required

web_bp = Blueprint("web", __name__)

def redirect_by_role():
    if current_user.role == ROLE_EMPLOYEE:
        return redirect(url_for("web.employee_dashboard"))
    if current_user.role == ROLE_MANAGER:
        return redirect(url_for("web.manager_dashboard"))
    if current_user.role == ROLE_ADMIN:
        return redirect(url_for("web.admin_dashboard"))
    abort(403)

@web_bp.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        return redirect_by_role()
    return redirect(url_for("web.login"))

@web_bp.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect_by_role()
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

@web_bp.route("/admin")
@login_required
@role_required(ROLE_ADMIN)
def admin_dashboard():
    return redirect(url_for("web.admin_users"))

@web_bp.route("/admin/users")
@login_required
@role_required(ROLE_ADMIN)
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin_users.html", users=users, roles=ROLE_OPTIONS)

@web_bp.route("/customers/new", methods=["GET"])
@login_required
def customer_new():
    return render_template("customer_form.html", categories=CUSTOMER_CATEGORIES)

@web_bp.route("/customers/<int:customer_id>")
@login_required
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    _ensure_customer_access(customer)
    interactions = (
        Interaction.query.filter_by(customer_id=customer.id)
        .order_by(Interaction.contact_date.desc())
        .all()
    )
    return render_template(
        "customer_detail.html",
        customer=customer,
        interactions=interactions,
    )

@web_bp.route("/customers/<int:customer_id>/edit", methods=["GET"])
@login_required
def customer_edit(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    _ensure_customer_access(customer)
    return render_template(
        "customer_form.html",
        customer=customer,
        categories=CUSTOMER_CATEGORIES,
    )