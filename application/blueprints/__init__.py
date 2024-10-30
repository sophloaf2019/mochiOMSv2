from application.blueprints.services import *
from application.blueprints.inventory import *
from application.blueprints.orders import *
from application.blueprints.users import *
from application.blueprints.routes import homepage_bp
from application.extensions import filters_bp


def register_blueprints(app):
    app.register_blueprint(homepage_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(filters_bp)
