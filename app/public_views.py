from app import app

import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

import stripe

stripe_keys = {
  'secret_key': app.config['STRIPE_SECRET_KEY'],
  'publishable_key': app.config['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

@app.route("/stripeindex", methods=["GET"])
def stripeindex():

	return render_template("public/stripeindex.html",key=stripe_keys['publishable_key'])


@app.route('/stripecharge', methods=['POST'])
def stripecharge():
	print("Amount : {}".format(amount))
	amount=request.form['amount']
	email=request.form['email']
	description=request.form['description']


	customer = stripe.Customer.create(
	    email=email,
	    source=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
	    customer=customer.id,
	    amount=amount,
	    currency='usd',
	    description=description
	)

	return render_template('public/stripecharge.html', amount=amount)


    