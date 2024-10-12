from flask import Flask
from application.extensions import db, migrate
from application.blueprints import register_blueprints
from application.blueprints.services.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    return app

