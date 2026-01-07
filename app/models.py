from datetime import datetime
from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customers = db.relationship("Customer", back_populates="created_by")
    interactions = db.relationship("Interaction", back_populates="user")

    def get_id(self):
        return str(self.id)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    category = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_by = db.relationship("User", back_populates="customers")
    interactions = db.relationship(
        "Interaction", back_populates="customer", cascade="all, delete-orphan"
    )

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    contact_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    no_response = db.Column(db.Boolean, default=False)

    customer = db.relationship("Customer", back_populates="interactions")
    user = db.relationship("User", back_populates="interactions")