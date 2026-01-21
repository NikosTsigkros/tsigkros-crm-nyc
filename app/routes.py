from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, logout_user

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
    return redirect(url_for("crm.login"))