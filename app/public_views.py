from app import app

import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("public/upload.html")