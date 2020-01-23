from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
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
from app import public_views,admin_views,jinja_views,jsonHTTPDockerlearning_views

