
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager




db = SQLAlchemy()
DB_NAME = 'users.db'


def create_app():

    #Configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is the key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #Register the blueprints

    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(views, url_prefix = '/')
    

    from .models import User
    #Database configurations
    db.init_app(app)
    create_database(app)

    #login manager configuration
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app



def create_database(app):
    if not os.path.exists('App/' + DB_NAME):
        db.create_all(app = app)
        print('Created Database')