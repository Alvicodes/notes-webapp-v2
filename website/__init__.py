from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
load_dotenv()

DB_KEY = os.getenv('DB')
SB_KEY = os.getenv('SuperBaseAccess')
SB_USER = os.getenv('SuperBaseUser')

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = DB_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres.{SB_USER}:{SB_KEY}@aws-0-eu-west-2.pooler.supabase.com:5432/postgres"
    db.init_app(app)

    # Migrate setup 
    migrate = Migrate(app, db)
    
    #registering blueprints with views/urls for app and location
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') # using only slash here as we dont want anything else in the prefix, keep it simple
    
    from .models import User, Note
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # similar to filter but looks for primary key
    
    return app

# # create function to check if database already exists
def create_database(app):
    if not path.exists('instance/' + DB_NAME): # using a path module to check if db exists
        with app.app_context():
            db.create_all() # create db if it doesn't exist
        print('Created Database!')
