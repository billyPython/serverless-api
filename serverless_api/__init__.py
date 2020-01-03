import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from . import config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.getenv("APP_SETTINGS", "serverless_api.config.DevelopmentConfig"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SERVER_NAME'] = 'localhost:5000'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # auth.py blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # base.py blueprint
    from .base import base as base_blueprint
    app.register_blueprint(base_blueprint)

    db.create_all(app=app)

    return app
