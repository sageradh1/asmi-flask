from app import app
from flask import render_template

@app.route("/")
def index():
	message ="Flask demo app is running."
	return render_template("public_views/index.html",message=message)