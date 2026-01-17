from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_login import current_user, request
from functools import wraps
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.string(100), unique=True)
    password = db.Column(db.string(200))
    role = db.Column(db.string(20), default="staff")
    is_admin = db.Column(db.Boolean, default=True)
    # admin | staff

    def is_admin(self):
        return self.role == "admin"
    
    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.is_admin():
                abort(403)
            return f(*args, **kwargs)
        return decorated

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Product(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.string(150))
    price = db.Column(db.Float)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def log_action(user, action, ip):
        log = AuditLog(
            user_id=user.id,
            action=action,
            ip_address=ip
        )
        db.session.add(log)
        db.session.commit()

    log_action(current_user, "CREATE PRODUCT", request.remote_addr)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    owner_id = db.Column(db.Integer)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total = db.Column(db.Float)
    status = db.Column(db.String(50)) # PENDING / PAID

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    method = db.Column(db.String(50))
    proof = db.Column(db.String(255))

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenant.id"))

    def get_current_tenant():
        return Tenant.query.get(current_user.tenant_id)