from app import app,db
from app.database.models import User,UserViewHistory,UploadedVideo
import random

query=User.query.order_by(User.id.asc())
alluserids = []
for eachuser in query:
	alluserids.append(eachuser.id)

query=UploadedVideo.query.order_by(UploadedVideo.videoid.asc())
alluploadedvideoids = []
for eachuploadedvideo in query:
	alluploadedvideoids.append(eachuploadedvideo.videoid)




for index in range(10000):
	
	id = db.Column(db.Integer, primary_key=True)
	user_id = random.choice(alluserids)
	watched_video_id = random.choice(alluploadedvideoids)
	watch_time_in_sec= random.randrange(0,300)
	_newuserviewhistory = UserViewHistory(user_id=user_id,watched_video_id=watched_video_id,watch_time_in_sec=watch_time_in_sec)
	db.session.add(_newuserviewhistory)

db.session.commit()