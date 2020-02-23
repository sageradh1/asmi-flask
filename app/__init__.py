from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
login.login_view = 'login'


#Loading databaase models
from app.database import models


# @login.request_loader
# def load_user(request):
#     token = request.headers.get('Authorization')
#     if token is None:
#         token = request.args.get('token')

#     if token is not None:
#         username,password = token.split(":") # naive token
#         user_entry = User.get(username)
#         if (user_entry is not None):
#             user = User(user_entry[0],user_entry[1])
#             if (user.password == password):
#                 return user
#     return None

#Loading views
#uncomment this jabir 
# from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views
# from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views,ad_views
from app import normal_views