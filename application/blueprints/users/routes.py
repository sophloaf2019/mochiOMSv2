from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from application.blueprints.users.models import User
from application.extensions import db, bcrypt

login_bp = Blueprint("login", __name__, template_folder="templates")


@login_bp.route("/login", methods=["POST"])
def login():
    data = request.form.to_dict()
    try:
        user = User.query.filter_by(username=data.get("username")).one()
    except Exception as e:
        user = None
    if user and bcrypt.check_password_hash(user.password, data.get("password")):
        login_user(user, remember=True)
        flash("Logged in successfully.", "success")
    else:
        flash("Username or password incorrect.", "danger")
    return redirect(url_for("homepage.homepage"))


@login_bp.route("/register", methods=["POST"])
def register():
    data = request.form.to_dict()

    user = User()

    user.first_name = data.get("first_name")
    user.last_name = data.get("last_name")
    user.email = data.get("email")
    user.phone_number = data.get("phone_number")
    user.username = data.get("username")
    user.password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    flash("Registered successfully.", "success")
    return redirect(url_for("homepage.homepage"))
