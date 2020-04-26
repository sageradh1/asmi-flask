from app import app,db
from flask import request,jsonify,make_response,redirect, render_template,flash,url_for,session

from app.forms import RegistrationForm,LoginForm,EditProfileForm,EditNewProfileForm

from flask_login import current_user, login_user,logout_user,login_required
from app.database.models import User,UploadedVideo,MergedAdCategory,VideoAnalyticsFile,Profile
# from app.utils.ad_prediction import get_appropriate_adids
# from app.utils.dataUtilsCode import dynamicJsonFile
# from sqlalchemy import exists,or_
# from sqlalchemy import in_


def returnNotSetIfNull(stringvariable):
	if stringvariable is None:
		return "not set"
	else:
		return stringvariable

def returnEmptyStringIfNull(stringvariable):
	if stringvariable is None:
		return ""
	else:
		return stringvariable

def returnZeroIfNull(stringvariable):
	if stringvariable is None:
		return 0
	else:
		return stringvariable

def returnZeroIfEmptyString(variable):
	if (variable is None) or (variable == ''):
		return 0
	else:
		return variable

@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		# return redirect(url_for('home'))
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")

	form = LoginForm()
	if form.validate_on_submit():
		try:
			user = User.query.filter_by(email=form.email.data).first()
			if user is None or not user.check_password(form.password.data):
				flash('Invalid username or password')
				return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")
			login_user(user, remember=True,duration=app.config["REMEMBER_COOKIE_DURATION"])
			# return redirect(url_for('home'))
			# return redirect("127.0.0.1:5000/home")
			return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")
		except Exception as err:
			# flash(err)
			flash("Problem while logging in.")
	return render_template('demo_views/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		# return redirect(url_for('home'))
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")
	form = RegistrationForm()

	redirectionDict = {
		"do_redirect":False,
		"redirection_url":app.config["BASE_URL_WITH_PORT"]+"/survey",	
	}

	if request.method=="GET":
		return render_template('demo_views/register.html', form=form,redirectionDict=redirectionDict)

	if request.method=="POST":
		if form.validate_on_submit():
			try:
				#All email and username duplication validation are handled while the form were created
				user = User(username=form.username.data, email=form.email.data)
				user.set_password(form.password.data)
				db.session.add(user)
				db.session.commit()


				profile = Profile(login_email=form.email.data,user_id=user.id)
				db.session.add(profile)
				db.session.commit()

				flash('Congratulations, you are now a registered user!')

				login_user(user, remember=True,duration=app.config["REMEMBER_COOKIE_DURATION"])

				redirectionDict["do_redirect"]=True

				return render_template('demo_views/register.html', form=form,redirectionDict=redirectionDict)
				# return redirect(app.config["BASE_URL_WITH_PORT"]+"/survey")
			except Exception as exp:
				print(exp)
				flash('Problem while registering user!')
				return render_template('demo_views/register.html', form=form,redirectionDict=redirectionDict)
		else:
			flash('Problem while validating data!')
			return render_template('demo_views/register.html', form=form,redirectionDict=redirectionDict)
	return render_template('demo_views/register.html', form=form,redirectionDict=redirectionDict)



familarity_map_object={-1: 'Choose...',
1: 'Extremely Familiar',
2: 'Very Familiar',
3: 'Somewhat Familiar',
4: 'Not So Familiar',
5: 'Not at all Familiar'
}

gender_map_object={
'0': 'M',
'1': 'F',
'2': 'O'
}



@app.route('/survey', methods=['GET', 'POST'])
# @login_required
def survey():
	userid=-1
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect("127.0.0.1:5000/login")
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

	redirectionDict = {
		"do_redirect":False,
		"redirection_url":app.config["BASE_URL_WITH_PORT"]+"/home",	
	}

	form = EditNewProfileForm()
		
	if request.method == 'GET':

		try:
			profile = Profile.query.filter_by(user_id=userid).first()
			form = EditNewProfileForm(obj=profile or None)
			return render_template('demo_views/survey.html',form=form)
		except Exception as err:
			print(err)
			form = EditNewProfileForm()
			return render_template('demo_views/survey.html',
				form=form,
				redirectionDict=redirectionDict
				)

	if request.method == 'POST':
		# print("Inside post")
		# print("Name: "+request.form['name'])
		# print("Age: "+request.form['age'])

		# if "gender" in request.form:
		# 	print(str(request.form['gender']))
		# else:
		# 	print("No gender")

		# if "is_user_content_creator" in request.form:
		# 	print(str(request.form['is_user_content_creator']))
		# else:
		# 	print("No is_user_content_creator")

		# print(request.form['contact_phone1'])
		# print(request.form['contact_email1'])

		# print(request.form['link_instagram'])
		# print(request.form['link_tiktok'])
		# print(request.form['link_firework'])
		# print(request.form['link_kwai'])

		# print(request.form['familarity_with_instagram'])
		# print(request.form['familarity_with_tiktok'])
		# print(request.form['familarity_with_kwai'])
		# print(request.form['familarity_with_triller'])

		# print(request.form['ideal_advertisers'])

		# print(request.form['number_of_followers_instagram'])
		# print(request.form['number_of_followers_tiktok'])
		# print(request.form['number_of_followers_triller'])
		# print(request.form['number_of_followers_kwai'])

	


		if form.validate_on_submit():
			print("successfully validated")
			try:
				profile = Profile.query.filter_by(user_id=userid).first()
				if profile is None:
					return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")

				profile.name=request.form['name']
				profile.age=request.form['age']


				if "gender" in request.form:
					profile.gender=str(gender_map_object[request.form['gender']])
				# profile.gender=request.form['gender']

				if "is_user_content_creator" in request.form:
					profile.is_user_content_creator =True
				else:
					profile.is_user_content_creator =False

				profile.contact_phone1=request.form['contact_phone1']
				profile.contact_email1=request.form['contact_email1']

				profile.link_instagram=request.form['link_instagram']
				profile.link_tiktok=request.form['link_tiktok']
				profile.link_firework=request.form['link_firework']
				profile.link_kwai=request.form['link_kwai']


				profile.familarity_with_instagram=request.form['familarity_with_instagram']
				profile.familarity_with_tiktok=   request.form['familarity_with_tiktok']
				profile.familarity_with_kwai=     request.form['familarity_with_kwai']
				profile.familarity_with_triller=  request.form['familarity_with_triller']

				profile.ideal_advertisers=request.form['ideal_advertisers']


				profile.number_of_followers_instagram=returnZeroIfEmptyString(request.form['number_of_followers_instagram'])
				profile.number_of_followers_tiktok=returnZeroIfEmptyString(request.form['number_of_followers_tiktok'])
				profile.number_of_followers_triller=returnZeroIfEmptyString(request.form['number_of_followers_triller'])
				profile.number_of_followers_kwai=returnZeroIfEmptyString(request.form['number_of_followers_kwai'])

				# profile.is_user_content_creator=request.form['is_user_content_creator']


				db.session.commit()

				# flash('Profile has been updated !')
				# print(profile.name)
				# print(profile.age)
				# print(profile.gender)
				
				# print(profile.contact_phone1)
				# print(profile.contact_email1)
				
				# print(profile.link_instagram)
				# print(profile.link_tiktok)
				# print(profile.link_instagram)
				# print(profile.link_tiktok)
				
				# print(profile.familarity_with_instagram)
				# print(profile.familarity_with_tiktok)
				# print(profile.familarity_with_firework)
				# print(profile.familarity_with_kwai)

				# print(profile.ideal_advertisers)
				# print(profile.reach)

				flash('Successfully submitted !')

				redirectionDict["do_redirect"]=True

				print(redirectionDict)
				form = EditNewProfileForm(obj=profile or None)
				return render_template('demo_views/survey.html',
					form=form,
					redirectionDict=redirectionDict
					)
			except Exception as err:
				print(err)
				flash('Problem while updating profile !')
				return render_template('demo_views/survey.html',
					form=form,
					redirectionDict=redirectionDict
					)
		else:
			print(form.errors)
			flash('Problem while validating profile !')
			return render_template('demo_views/survey.html',
					form=form,
					redirectionDict=redirectionDict
					)


	return render_template('demo_views/survey.html',
					form=form,
					redirectionDict=redirectionDict
					)

@app.route('/logout')
# @login_required
def logout():
	if current_user.is_authenticated:
	    logout_user()
	# return redirect("127.0.0.1:5000/login")
	# return redirect(url_for('home'))
	return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

@app.route('/')
@app.route('/home')
# @login_required
def home():
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect("127.0.0.1:5000/login")
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

	try:
		c=db.session.query(UploadedVideo).order_by(UploadedVideo.videoid.desc()).limit(1)
		latestvideoid = c[0].videoid
	except:
		latestvideoid=-1
	view_video_url=str(app.config["BASE_URL_WITH_PORT"]+"/demoviewvideos")

	# print(view_video_url)
	return render_template('demo_views/home.html', view_video_url=view_video_url,current_username=current_user.username)

# @app.route('/viewRaghivvide')
# # @login_required
# def viewRaghivvide():
# 	return render_template('demo_views/viewvideo.html',main_video_url=main_video_url)




@app.route('/view-profile')
# @login_required
def view_profile():
	userid=-1
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect("127.0.0.1:5000/login")
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

	try:
		profile = Profile.query.filter_by(user_id=userid).first()
		if profile is None:
			return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")
		name = profile.name
		# dob=profile.dob
		age=profile.age
		login_email = profile.login_email
		contact_phone1 = profile.contact_phone1
		contact_email1 = profile.contact_email1
		
		link_instagram= profile.link_instagram
		link_tiktok= profile.link_tiktok
		link_firework= profile.link_firework
		link_kwai= profile.link_kwai
		
		ideal_advertisers =  profile.ideal_advertisers

		number_of_followers_instagram= profile.number_of_followers_instagram
		number_of_followers_tiktok= profile.number_of_followers_tiktok
		number_of_followers_triller= profile.number_of_followers_triller
		number_of_followers_kwai= profile.number_of_followers_kwai

		# insta_reach = profile.reach

		user_id= profile.user_id


		return render_template('demo_views/view-profile.html',
			name=returnNotSetIfNull(name),
			age=returnNotSetIfNull(age),
			login_email =returnNotSetIfNull(login_email),
			contact_phone1=returnNotSetIfNull(contact_phone1),
			contact_email1=returnNotSetIfNull(contact_email1),
			link_instagram=returnEmptyStringIfNull(link_instagram),
			link_tiktok=returnEmptyStringIfNull(link_tiktok),
			link_firework=returnEmptyStringIfNull(link_firework),
			link_kwai=returnEmptyStringIfNull(link_kwai),
			ideal_advertisers=returnNotSetIfNull(ideal_advertisers),
			number_of_followers_instagram=returnZeroIfNull(number_of_followers_instagram),
			number_of_followers_tiktok=returnZeroIfNull(number_of_followers_tiktok),
			number_of_followers_triller=returnZeroIfNull(number_of_followers_triller),
			number_of_followers_kwai=returnZeroIfNull(number_of_followers_kwai)
			)
	except Exception as err:
		print(err)
		return render_template('demo_views/view-profile.html',
			name="" ,
			age="",
			login_email ="",
			contact_phone1="",
			contact_email1="",
			link_instagram="",
			link_tiktok="",
			link_firework="",
			link_kwai="",
			ideal_advertisers="",
			number_of_followers_instagram="",
			number_of_followers_tiktok="",
			number_of_followers_triller="",
			number_of_followers_kwai=""
			)
# profile_id = db.Column(db.Integer, primary_key=True)
# name = db.Column(db.String(120))
# dob=db.Column(db.DateTime, index=True)
# login_email = db.Column(db.String(120))
# contact_phone1 = db.Column(db.String(20))
# contact_email1 = db.Column(db.String(120))
# link_instagram = db.Column(db.String(500))
# link_tiktok = db.Column(db.String(500))
# ideal_advertisers =  db.Column(db.String(1000))
# reach = db.Column(db.Integer)
# user_id= db.Column(db.Integer)



@app.route('/edit-profile', methods=['GET','POST'])
# @login_required
def edit_profile():
	userid=-1
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect("127.0.0.1:5000/login")
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

	if request.method == 'GET':
		try:
			profile = Profile.query.filter_by(user_id=userid).first()
			if profile is None:
				return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")



			form = EditProfileForm(obj=profile)
			return render_template('demo_views/edit-profile.html',
				form=form
				)
		except Exception as err:
			print(err)
			form = EditProfileForm()
			return render_template('demo_views/edit-profile.html',
				form=form,
				)

	if request.method == 'POST':
		try:
			profile = Profile.query.filter_by(user_id=userid).first()
			if profile is None:
				return redirect(app.config["BASE_URL_WITH_PORT"]+"/home")

			profile.name=request.form['name']
			# profile.dob=request.form['dob']
			profile.age=request.form['age']
			profile.contact_phone1=request.form['contact_phone1']
			profile.contact_email1=request.form['contact_email1']

			profile.link_instagram=request.form['link_instagram']
			profile.link_tiktok=request.form['link_tiktok']
			profile.ideal_advertisers=request.form['ideal_advertisers']
			profile.number_of_followers_instagram=request.form['number_of_followers_instagram']
			profile.number_of_followers_tiktok=request.form['number_of_followers_tiktok']

			db.session.commit()

			flash('Profile has been updated !')
			# print(name)
			# print(dob)
			# print(contact_phone1)
			# print(contact_email1)
			# print(link_instagram)
			# print(link_tiktok)
			# print(ideal_advertisers)
			# print(reach)


			form = EditProfileForm(obj=profile)
			return render_template('demo_views/edit-profile.html',
				form=form
				)
		except Exception as err:
			print(err)
			flash('Problem while updating profile !')
			return redirect(app.config["BASE_URL_WITH_PORT"]+"/edit-profile")







	# name=request.form['name']
	# amount=request.form['amount']
	# email=request.form['email']
	# description=request.form['description']





@app.route('/demoviewvideos')
# @login_required
def demoviewvideos():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")
	else:
		userid=current_user.id
	
	filename="20200229134607AngreziMediumLowerQuality.mp4"
	# main_video_url=request.url_root+str("static/video/uploaded/")+str(filename)
	main_video_url=app.config["BASE_URL_WITH_PORT"]+"/"+str("static/video/uploaded/")+str(filename)
	print(main_video_url)
	return render_template('demo_views/viewvideo.html',main_video_url=main_video_url)



@app.route('/2d')
def view_2d():
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect("127.0.0.1:5000/login")
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")

	filename="20200229134607AngreziLowerQuality.mp4"
	# main_video_url=request.url_root+str("static/video/uploaded/")+str(filename)
	main_video_url=app.config["BASE_URL_WITH_PORT"]+"/"+str("static/video/uploaded/")+str(filename)
	print(main_video_url)
	return render_template('demo_views/2dview.html',main_video_url=main_video_url,current_username=current_user.username)

@app.route('/3d')
def view_3d():
	return render_template('demo_views/3dview.html')

import json
@app.route('/api/GetStaticJson',methods=['POST'])
def getstaticjson():

	# main_video_url=request.url_root+str("static/video/uploaded/")+str(filename)
	static_json="/home/ubuntu/workingDir/asmi-flask/app/static/analyticsFolder/generated/demo-raw1.json"
	data=dict()
	try:
		with open(static_json) as blog_file:
			data = json.load(blog_file)
	except Exception as err:
		return jsonify({"message":"Error","data":str(err)})

	return jsonify({"message":"Success","data":data})

@app.route('/uploaded')
# @login_required
def uploaded():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")
	latestvideoList=UploadedVideo.query.order_by(UploadedVideo.videoid.desc()).limit(15)
	if latestvideoList is None:
		latestvideoList=[]

	return render_template('demo_views/uploaded.html',latestvideoList=latestvideoList,current_username=current_user.username)


@app.route('/analytics')
# @login_required
def analytics():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect(app.config["BASE_URL_WITH_PORT"]+"/login")
	analyticsFileList=VideoAnalyticsFile.query.order_by(VideoAnalyticsFile.analyticsfileid.desc()).limit(15)
	if analyticsFileList is None:
		analyticsFileList=[]

	return render_template('demo_views/analytics.html',analyticsFileList=analyticsFileList,current_username=current_user.username)

