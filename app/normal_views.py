from app import app,db
from flask import request,jsonify,make_response,redirect, render_template,flash,url_for

from app.forms import RegistrationForm,LoginForm

from flask_login import current_user, login_user,logout_user,login_required
from app.database.models import User
# from sqlalchemy import exists,or_

@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		try:
			user = User.query.filter_by(email=form.email.data).first()
			if user is None or not user.check_password(form.password.data):
				flash('Invalid username or password')
				return redirect(url_for('login'))
			login_user(user, remember=True)
			return redirect(url_for('home'))
		except Exception as err:
			# flash(err)
			flash("Problem while logging in.")
	return render_template('normal_views/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()

	if request.method=="GET":
		return render_template('normal_views/register.html', form=form)

	if request.method=="POST":
		if form.validate_on_submit():
			try:
				# doesEmailorUsernameExits = db.session.query(exists().where(or_(User.email==form.email.data,User.username==form.username.data))).scalar()
				# if doesEmailorUsernameExits:
				# 	doesEmailMatch = db.session.query(exists().where(User.email==form.email.data)).scalar()
				# 	if doesEmailMatch:
				# 		flash('The email already exists!')
				# 		return render_template('normal_views/register.html', form=form)

				# 	doesUsernameMatch = db.session.query(exists().where(User.username==form.username.data)).scalar()
				# 	if doesUsernameMatch:
				# 		flash('The username already exists!')
				# 		return render_template('normal_views/register.html', form=form)
			
				user = User(username=form.username.data, email=form.email.data)
				user.set_password(form.password.data)
				db.session.add(user)
				db.session.commit()
				flash('Congratulations, you are now a registered user!')
				return render_template('normal_views/register.html', form=form)
			except Exception as exp:
				flash('Problem, while registering user!')
				return render_template('normal_views/register.html', form=form)
		else:
			flash('Problem, while validating data!')
			return render_template('normal_views/register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
@login_required
def home():
    # show the user profile for that user
    return "homepage loaded"


# @app.route('/eachuser/<username>')
# def eachuser(username):
#     # show the user profile for that user
#     return 'User %s' % username