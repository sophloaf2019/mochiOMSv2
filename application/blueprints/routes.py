from flask import Blueprint, render_template
from flask_login import current_user
from application.extensions import jp

homepage_bp = Blueprint("homepage", __name__, template_folder="templates")


@homepage_bp.route("/")
def homepage():
    if not current_user:
        return jp.render("homepage.html")
    else:
        return jp.render("dashboard.html")


@homepage_bp.route("/jinjax")
def jinjaxtest():
    return catalog.render("PageLayout", active_link="services")
