class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://mochi_user:secure@localhost/mochioms_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False