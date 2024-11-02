from flask import Blueprint, render_template
from flask_login import current_user

homepage_bp = Blueprint("homepage", __name__, template_folder="templates")


@homepage_bp.route("/")
def homepage():
    if not current_user:
        return render_template("homepage.html")
    else:
        return render_template("dashboard.html")
