from functools import wraps
from flask_login import current_user, login_manager
from flask import abort

from app.constants import ROLE_EMPLOYEE

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not current_user.active:
                abort(403)
            if current_user.role not in roles:
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator

def _ensure_customer_access(customer):
    if current_user.role == ROLE_EMPLOYEE and customer.created_by_id != current_user.id:
        abort(403)