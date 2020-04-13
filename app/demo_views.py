from app import app,db
from flask import request,jsonify,make_response,redirect, render_template,flash,url_for,session

from app.forms import RegistrationForm,LoginForm

from flask_login import current_user, login_user,logout_user,login_required
from app.database.models import User,UploadedVideo,MergedAdCategory,VideoAnalyticsFile
# from app.utils.ad_prediction import get_appropriate_adids
# from app.utils.dataUtilsCode import dynamicJsonFile
# from sqlalchemy import exists,or_
# from sqlalchemy import in_


@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		# return redirect(url_for('home'))
		return redirect("http://18.221.137.201/home")

	form = LoginForm()
	if form.validate_on_submit():
		try:
			user = User.query.filter_by(email=form.email.data).first()
			if user is None or not user.check_password(form.password.data):
				flash('Invalid username or password')
				return redirect(url_for('login'))
			login_user(user, remember=True,duration=app.config["REMEMBER_COOKIE_DURATION"])
			# return redirect(url_for('home'))
			return redirect("http://18.221.137.201/home")
		except Exception as err:
			# flash(err)
			flash("Problem while logging in.")
	return render_template('demo_views/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		# return redirect(url_for('home'))
		return redirect("http://18.221.137.201/home")
	form = RegistrationForm()

	if request.method=="GET":
		return render_template('demo_views/register.html', form=form)

	if request.method=="POST":
		if form.validate_on_submit():
			try:
				user = User(username=form.username.data, email=form.email.data)
				user.set_password(form.password.data)
				db.session.add(user)
				db.session.commit()
				flash('Congratulations, you are now a registered user!')
				return render_template('demo_views/register.html', form=form)
			except Exception as exp:
				flash('Problem while registering user!')
				return render_template('demo_views/register.html', form=form)
		else:
			flash('Problem while validating data!')
			return render_template('demo_views/register.html', form=form)


@app.route('/logout')
# @login_required
def logout():
	if current_user.is_authenticated:
	    logout_user()
	# return redirect(url_for('home'))
	return redirect("http://18.221.137.201/login")

@app.route('/')
@app.route('/home')
# @login_required
def home():
	if current_user.is_authenticated:
		userid=current_user.id
	else:
		# return redirect(url_for('login'))
		return redirect("http://18.221.137.201/login")

	try:
		c=db.session.query(UploadedVideo).order_by(UploadedVideo.videoid.desc()).limit(1)
		latestvideoid = c[0].videoid
	except:
		latestvideoid=-1
	view_video_url=str('http://18.221.137.201/demoviewvideos')
	# print(view_video_url)
	return render_template('demo_views/home.html', view_video_url=view_video_url)

# @app.route('/viewRaghivvide')
# # @login_required
# def viewRaghivvide():
# 	return render_template('demo_views/viewvideo.html',main_video_url=main_video_url)

@app.route('/demoviewvideos')
# @login_required
def demoviewvideos():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect("http://18.221.137.201/login")
	else:
		userid=current_user.id
	
	filename="20200229134607AngreziMediumLowerQuality.mp4"
	# main_video_url=request.url_root+str("static/video/uploaded/")+str(filename)
	main_video_url="http://18.221.137.201/"+str("static/video/uploaded/")+str(filename)
	print(main_video_url)
	return render_template('demo_views/viewvideo.html',main_video_url=main_video_url)



@app.route('/2d')
def view_2d():

	filename="20200229134607AngreziLowerQuality.mp4"
	# main_video_url=request.url_root+str("static/video/uploaded/")+str(filename)
	main_video_url="http://18.221.137.201/"+str("static/video/uploaded/")+str(filename)
	print(main_video_url)
	return render_template('demo_views/2dview.html',main_video_url=main_video_url)

@app.route('/3d')
def view_3d():
	return render_template('demo_views/3dview.html')

@app.route('/uploaded')
# @login_required
def uploaded():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect("http://18.221.137.201/login")
	latestvideoList=UploadedVideo.query.order_by(UploadedVideo.videoid.desc()).limit(15)
	if latestvideoList is None:
		latestvideoList=[]

	return render_template('demo_views/uploaded.html',latestvideoList=latestvideoList)


@app.route('/analytics')
# @login_required
def analytics():
	if not current_user.is_authenticated:
		# return redirect(url_for('login'))
		return redirect("http://18.221.137.201/login")
	analyticsFileList=VideoAnalyticsFile.query.order_by(VideoAnalyticsFile.analyticsfileid.desc()).limit(15)
	if analyticsFileList is None:
		analyticsFileList=[]

	return render_template('demo_views/analytics.html',analyticsFileList=analyticsFileList)

