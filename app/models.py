from datetime import datetime
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
