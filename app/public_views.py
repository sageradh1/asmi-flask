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

@app.route("/stripe-index", methods=["GET"])
def stripeindex():
	return render_template("public/stripe-index.html",key=stripe_keys['publishable_key'])


@app.route('/stripe-create-pi', methods=['POST'])
def stripecharge():
	name=request.form['name']
	amount=request.form['amount']
	email=request.form['email']
	description=request.form['description']

	intent = stripe.PaymentIntent.create(
	  amount=amount,
	  currency='usd',
	)

	# print(intent["client_secret"])

	# customer = stripe.Customer.create(
	#     email=email,
	#     source=request.form['stripeToken']
	# )

	# charge = stripe.Charge.create(
	#     customer=customer.id,
	#     amount=amount,
	#     currency='usd',
	#     description=description
	# )

	return render_template('public/stripe-create-pi.html', amount=amount,pub_key=stripe_keys['publishable_key'],client_secret=intent["client_secret"],customer_name=name)
	# return render_template('public/stripe-create-pi.html', amount=amount,client_secret=client_secret)





# Region STRIPE DOCUMENTED 
# @app.route('/', methods=['GET'])
# def get_setup_intent_page():
#     return render_template('public/stripe-modal.html')

# @app.route('/public-key', methods=['GET'])
# def get_publishable_key():
#     return jsonify(publicKey=app.config['STRIPE_PUBLISHABLE_KEY'])

# def calculate_order_amount(items):
#     # Replace this constant with a calculation of the order's amount
#     # Calculate the order total on the server to prevent
#     # people from directly manipulating the amount on the client
#     return 1999


# @app.route('/payment_intents', methods=['POST'])
# def create_payment_intent():
#     # Reads application/json and returns a response
#     data = json.loads(request.data)
#     payment_intent = stripe.PaymentIntent.create(
#         amount=calculate_order_amount(data['items']),
#         currency=data['currency'],
#     )
#     return jsonify(payment_intent)


# @app.route('/webhook', methods=['POST'])
# def webhook_received():
#     # You can use webhooks to receive information about asynchronous payment events.
#     # For more about our webhook events check out https://stripe.com/docs/webhooks.
#     webhook_secret = app.config['STRIPE_WEBHOOK_SECRET']
#     request_data = json.loads(request.data)

#     if webhook_secret:
#         # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
#         signature = request.headers.get('stripe-signature')
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload=request.data, sig_header=signature, secret=webhook_secret)
#             data = event['data']
#         except Exception as e:
#             return e
#         # Get the type of webhook event sent - used to check the status of PaymentIntents.
#         event_type = event['type']
#     else:
#         data = request_data['data']
#         event_type = request_data['type']
#     data_object = data['object']

#     if event_type == 'payment_intent.succeeded':
#         print('🔔 Occurs when a new SetupIntent is created.')

#     return jsonify({'status': 'success'})
# # Endregion


