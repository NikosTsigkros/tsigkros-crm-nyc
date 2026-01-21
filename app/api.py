from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

from .models import User

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
        return redirect(url_for("crm.index"))
    flash("Invalid credentials or inactive account.", "error")
