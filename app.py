from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, admin_required
from config import Config
from extensions import db, login_manager
from models import User, Product
from forms import LoginForm, ProductForm, UserForm
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.config["JWT_SECRET_KEY"] = "jwt-secret"
jwt = JWTManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        admin = User(username="admin")
        admin.set_password("MaungBhoneHtet12")
        db.session.add(admin)
        db.session.commit()

@app.route("/", method=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        return render_template("auth/login.html", form=form)
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")

@app.route("/product")
@login_required
def products():
    return render_template(
        "admin/products.html",
        products=Product.query.all()
    )

@app.route("/products/create", methods=["GET", "POST"])
@login_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("products"))
    return render_template("admin/product_form.html", form=form)

@app.route("/products/delete/<int:id>")
@login_required
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products"))

@app.route("/admin-only")
@admin_required
def admin_only():
    return "Admin Access"

@app.route("/users")
@admin_required
def users():
    return render_template("admin/users.html", users=User.query.all())

@app.route("/users/create", methods=["GET", "POST"])
@admin_required
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users"))
    return render_template("admin/user_form.html", form=form)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return {"access_token": token}
    return {"error": "Invalid"}, 401

@app.route("/api/products")
@jwt_required()
def api_products():
    return {"products": [
        {"name": p.name, "price": p.price}
        for p in Product.query.all()
    ]}

@app.route("/api/upload", methods=["POST"])
@jwt_required()
def upload():
    file = request.files["file"]
    file.save(f"uploads/{file.filename}")
    return {"success": True}