from collections import defaultdict
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.constants import CUSTOMER_CATEGORIES, ROLE_ADMIN, ROLE_ADMIN, ROLE_EMPLOYEE, ROLE_MANAGER, ROLE_OPTIONS
from app.utils import _ensure_customer_access, role_required

from .models import Customer, Interaction, User
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
    return redirect(url_for("web.login"))

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
        return redirect(url_for("web.customers"))
    
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
        return redirect(url_for("web.admin_users"))
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
    return redirect(url_for("web.admin_users"))

@api_bp.route("/customers/<int:customer_id>/edit", methods=["POST"])
@login_required
def customer_edit(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    _ensure_customer_access(customer)
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    category = request.form.get("category", customer.category)
    active = request.form.get("active") == "on"
    if not name:
        flash("Name is required.", "error")
    elif category not in CUSTOMER_CATEGORIES:
        flash("Invalid category.", "error")
    else:
        customer.name = name
        customer.email = email
        customer.phone = phone
        customer.category = category
        customer.active = active
        db.session.commit()
        flash("Customer updated.", "success")
        return redirect(url_for("web.customer_detail", customer_id=customer.id))
    
@api_bp.route("/customers/<int:customer_id>/disable", methods=["POST"])
@login_required
def customer_disable(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    _ensure_customer_access(customer)
    customer.active = False
    db.session.commit()
    flash("Customer disabled.", "success")
    return redirect(url_for("web.customers"))

@api_bp.route("/customers/<int:customer_id>/interactions/new", methods=["POST"])
@login_required
def interaction_new(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    _ensure_customer_access(customer)
    notes = request.form.get("notes", "").strip()
    no_response = request.form.get("no_response") == "on"
    interaction = Interaction(
        customer_id=customer.id,
        user_id=current_user.id,
        notes=notes,
        no_response=no_response,
        contact_date=datetime.utcnow(),
    )
    db.session.add(interaction)
    db.session.commit()
    flash("Interaction logged.", "success")
    return redirect(url_for("web.customer_detail", customer_id=customer.id))

@api_bp.route("/employee/stats")
@login_required
@role_required(ROLE_EMPLOYEE)
def api_employee_stats():
    now = datetime.utcnow()
    day = now - timedelta(days=1)
    week = now - timedelta(days=7)
    month = now - timedelta(days=30)

    customers_added = Customer.query.filter_by(created_by_id=current_user.id).count()
    interactions = Interaction.query.filter_by(user_id=current_user.id)
    stats = {
        "customersAdded": customers_added,
        "contactsLastDay": interactions.filter(Interaction.contact_date >= day).count(),
        "contactsLastWeek": interactions.filter(Interaction.contact_date >= week).count(),
        "contactsLastMonth": interactions.filter(
            Interaction.contact_date >= month
        ).count(),
    }
    return jsonify(stats)

@api_bp.route("/manager/stats")
@login_required
@role_required(ROLE_MANAGER)
def api_manager_stats():
    days = int(request.args.get("days", 30))
    days = max(1, min(days, 365))
    no_response_n = int(request.args.get("no_response_n", 5))
    no_response_n = max(1, min(no_response_n, 20))
    since = datetime.utcnow() - timedelta(days=days)

    contacts_per_employee = defaultdict(int)
    interactions = Interaction.query.filter(Interaction.contact_date >= since).all()
    for interaction in interactions:
        contacts_per_employee[interaction.user.username] += 1

    last_contact = (
        db.session.query(Customer, db.func.max(Interaction.contact_date))
        .outerjoin(Interaction)
        .group_by(Customer.id)
        .all()
    )
    inactive_customers = [
        {
            "id": customer.id,
            "name": customer.name,
            "lastContact": last_date.isoformat() if last_date else "Never",
        }
        for customer, last_date in last_contact
        if not last_date or last_date < since
    ]

    no_response_customers = []
    for customer in Customer.query.all():
        recent = (
            Interaction.query.filter_by(customer_id=customer.id)
            .order_by(Interaction.contact_date.desc())
            .limit(no_response_n)
            .all()
        )
        if recent and all(inter.no_response for inter in recent):
            no_response_customers.append({"id": customer.id, "name": customer.name})

    category_counts = defaultdict(int)
    for customer in Customer.query.filter(Customer.created_at >= since).all():
        category_counts[customer.category] += 1

    response = {
        "contactsPerEmployee": [
            {"employee": name, "count": count}
            for name, count in contacts_per_employee.items()
        ],
        "inactiveCustomers": inactive_customers,
        "noResponseCustomers": no_response_customers,
        "categoryCounts": category_counts,
    }
    return jsonify(response)