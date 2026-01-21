from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash

from app.constants import CUSTOMER_CATEGORIES

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