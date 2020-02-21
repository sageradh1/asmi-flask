from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

#Loading environment from .startingenv
import os
from dotenv import load_dotenv
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


#Loading databaase models
from app.database import models

#Loading views
#uncomment this jabir 
# from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views
from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views,ad_views