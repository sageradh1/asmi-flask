from app import app,db
from flask import request,jsonify,make_response,redirect, render_template,flash,url_for,session

from app.forms import RegistrationForm,LoginForm

from flask_login import current_user, login_user,logout_user,login_required
from app.database.models import User,UploadedVideo,MergedAdCategory,VideoAnalyticsFile
from app.utils.ad_prediction import get_appropriate_adids
from app.utils.dataUtilsCode import dynamicJsonFile
# from sqlalchemy import exists,or_
# from sqlalchemy import in_

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_views/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error_views/500.html'), 500


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
			login_user(user, remember=True,duration=app.config["REMEMBER_COOKIE_DURATION"])
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
				flash('Problem while registering user!')
				return render_template('normal_views/register.html', form=form)
		else:
			flash('Problem while validating data!')
			return render_template('normal_views/register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
@login_required
def home():

	if current_user.is_authenticated:
		userid=current_user.id
	else:
		userid=-1
	try:
		c=db.session.query(UploadedVideo).order_by(UploadedVideo.videoid.desc()).limit(1)
		latestvideoid = c[0].videoid
	except:
		latestvideoid=-1
	view_video_url=request.url_root+str(url_for('viewvideos'))[1:]+"?userid="+str(userid)+"&videoid="+str(latestvideoid)
	return render_template('normal_views/home.html', view_video_url=view_video_url)


@app.route('/viewvideos')
@login_required
def viewvideos():

	userid = request.args.get('userid')
	videoid = request.args.get('videoid')

	if userid is None:
		print("userid is none")
		userid=current_user.id

	latestvideoList=[]
	dynamicJson=[]
	try:

		# latestvideoList=db.session.query(UploadedVideo).order_by(UploadedVideo.videoid.desc()).limit(5)
		latestvideoList=UploadedVideo.query.order_by(UploadedVideo.videoid.desc()).limit(5)
		# for video in latestvideoList:
		#     print(video.detected_objects_withconfidence)
		if videoid is None:
			videoid = latestvideoList[0].videoid
		
		userid=8
		videoid=10056
		adnames =get_appropriate_adids(userid,videoid)
		mergedAdCategories=db.session.query(MergedAdCategory).filter(MergedAdCategory.category_name.in_(adnames))
		# print(mergedAdCategories.count())

		requiredObjectLabels=[]
		for mergedAdCategory in mergedAdCategories:
		    requiredObjectLabels.append(mergedAdCategory.category_name)
		# for i in range(len(mergedAdCategories)):
		# 	print(mergedAdCategories[i])
		print(requiredObjectLabels)

		print("video id :",videoid)
		analytics_file =  VideoAnalyticsFile.query.filter_by(video_id=videoid).first()
		if analytics_file is None:
			print("No analytics_file found.")
			return render_template('normal_views/viewvideo.html',latestvideoList=latestvideoList)

		_filename=analytics_file.filename
		# requiredObjectLabels = ['train','Shirt']

		dynamicJson = dynamicJsonFile(_filename,requiredObjectLabels)
		print(dynamicJson)
	except Exception as err:
		latestvideoid=-1
		print("Error : ",err)

	return render_template('normal_views/viewvideo.html',latestvideoList=latestvideoList,dynamicJson=dynamicJson)




# @app.route('/eachuser/<username>')
# def eachuser(username):
#     # show the user profile for that user
#     return 'User %s' % username