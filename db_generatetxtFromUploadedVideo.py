from app import db
from app.database.models import UploadedVideo
import random

query=UploadedVideo.query.order_by(UploadedVideo.videoid.asc())

f = open("app/static/database-asmi/uploadedVideos.txt", "w")
f.write("video_id,detected_objects_withconfidence\n")

for eachCategory in query:
	f.write(str(eachCategory.videoid)+","+eachCategory.detected_objects_withconfidence)
	f.write("\n")
f.close()