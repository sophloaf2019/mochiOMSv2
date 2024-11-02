from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from application.extensions import db, migrate, bcrypt, login_manager
from application.blueprints import *
from flask_login import LoginManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__, template_folder="components")
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    CORS(app)
    login_manager.init_app(app)
    login_manager.login_view = 'homepage.homepage'

    register_blueprints(app)
    
    with app.app_context():
        from application.blueprints.users.models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)
        # db.drop_all()
        db.create_all()
        
    @app.route('/')
    @app.route('/<path:path>')
    def serve_vue(path=""):
        return send_from_directory(app.static_folder, 'index.html')
    return app

