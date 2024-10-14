from flask import Blueprint, render_template

orders_bp = Blueprint('orders', __name__, url_prefix='/orders', template_folder='templates')