from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

import os
from dotenv import load_dotenv

from flask_login import LoginManager


app = Flask(__name__)

#Loading environment from .startingenv
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.startingenv')
load_dotenv(dotenv_path)

app.config["APP"] = os.getenv('FLASK_APP')
app.config["ENV"] = os.getenv('FLASK_ENV')
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)

#Loading which configuration to use
if app.config["ENV"]=="development":
    app.config.from_object("config.DevelopmentConfig")
elif app.config["ENV"]=="testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

print("The environment is : "+app.config["ENV"])
print(f"The current database being used is : ${app.config['DB_NAME']} ")

#Loading db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Loading login manager 
login = LoginManager(app)
login.login_view = 'http://18.221.137.201/login'


# Setting timeout for session cookie (It is not a setting for remember_token cookie set by flask_login)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = app.config["REMEMBER_COOKIE_DURATION"]

#Loading databaase models
from app.database import models

#Loading views
#uncomment this jabir 
# from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views
# from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views,normal_views
# from app import normal_views,jsonHTTPDockerlearning_views
from app import demo_views,jsonHTTPDockerlearning_views
# from app import demo_normal_views