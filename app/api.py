from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.constants import CUSTOMER_CATEGORIES, ROLE_ADMIN, ROLE_ADMIN, ROLE_EMPLOYEE, ROLE_OPTIONS
from app.utils import role_required

from .models import Customer, User
from . import db

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/ping")
def ping():
    return jsonify(message="Pong from Flask!")

@api_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = User.query.filter_by(username=username).first()
    if user and user.active and check_password_hash(user.password_hash, password):
        login_user(user)
        return redirect(url_for("web.index"))
    flash("Invalid credentials or inactive account.", "error")

@api_bp.route("/customers/new", methods=["POST"])
@login_required
def customer_new():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    category = request.form.get("category", "Lead")
    if not name:
        flash("Name is required.", "error")
    elif category not in CUSTOMER_CATEGORIES:
        flash("Invalid category.", "error")
    else:
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            category=category,
            created_by_id=current_user.id,
        )
        db.session.add(customer)
        db.session.commit()
        flash("Customer created.", "success")
        return redirect(url_for("crm.customers"))
    
@api_bp.route("/admin/users/new", methods=["POST"])
@login_required
@role_required(ROLE_ADMIN)
def admin_user_new():
    username = request.form.get("username", "").strip()
    role = request.form.get("role", ROLE_EMPLOYEE)
    password = request.form.get("password", "")
    if not username or not password:
        flash("Username and password required.", "error")
    elif role not in ROLE_OPTIONS:
        flash("Invalid role.", "error")
    elif User.query.filter_by(username=username).first():
        flash("Username already exists.", "error")
    else:
        user = User(
            username=username,
            role=role,
            active=True,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        flash("User created.", "success")
    return redirect(url_for("web.admin_users"))

@api_bp.route("/admin/users/<int:user_id>/edit", methods=["POST"])
@login_required
@role_required(ROLE_ADMIN)
def admin_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot edit your own role or status.", "error")
        return redirect(url_for("crm.admin_users"))
    role = request.form.get("role", user.role)
    active = request.form.get("active") == "on"
    password = request.form.get("password")
    if role not in ROLE_OPTIONS:
        flash("Invalid role.", "error")
    else:
        user.role = role
        user.active = active
        if password:
            user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash("User updated.", "success")
    return redirect(url_for("crm.admin_users"))