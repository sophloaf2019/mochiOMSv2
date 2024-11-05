from flask import Blueprint, render_template
from application.extensions import jp

orders_bp = Blueprint(
    "orders", __name__, url_prefix="/orders", template_folder="templates"
)


@orders_bp.route("/")
def homepage():
    return jp.render("orders_homepage.html")


@orders_bp.route("/new_order")
def new_order():
    return jp.render("orders_new_order.html")
