from app import db
# from app.database.models import MergedAdCategory,UploadedVideo
from app.database.models import UserViewHistory
import random

query=UserViewHistory.query.order_by(UserViewHistory.id.asc())

f = open("userViewHistories.txt", "w")
f.write("id,user_id,watched_video_id,watch_time_in_sec\n")

for eachCategory in query:
	f.write(str(eachCategory.id)+","+str(eachCategory.user_id)+","+str(eachCategory.watched_video_id)+","+str(eachCategory.watch_time_in_sec)+"\n")
f.close()