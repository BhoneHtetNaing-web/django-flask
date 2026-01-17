from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from flask_login import current_user
from functools import wraps

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
