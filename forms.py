from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Product Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password")
    role = StringField("Role (admin/staff)")