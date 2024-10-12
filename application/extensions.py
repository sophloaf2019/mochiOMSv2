from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a single instance of SQLAlchemy to be used across the app
db = SQLAlchemy()
migrate = Migrate()