from app import app,db
from app.database.models import MergedAdCategory,UploadedVideo,User
import random

query=MergedAdCategory.query.order_by(MergedAdCategory.id.asc()).limit(10)

allcategories = []
for eachrow in query:
	allcategories.append(eachrow.category_name)

# Generating confidence as from 0 to 1
confidenceScoreList=[]
for i in range(1,len(allcategories)+1):
	confidenceScoreList.append(i/(len(allcategories)))
# print(confidenceScoreList)
# [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]




allusers=User.query.order_by(User.id.asc())
userids=[]
for user in allusers:
	userids.append(user.id)
# print(userids)


# # for index in range(10000):
for index in range(50):

	filename = "testvideo"+str(index)
	extension = "mp4"
	storagelocation = app.config["VIDEO_UPLOADS_FOLDER"]
	detected_objects_withconfidence=""

	eachloopScoreList =confidenceScoreList.copy()
	

	finalstring=""
	for eachcategory in allcategories:
		randomconfidence= random.choice(eachloopScoreList)

		if len(eachloopScoreList)>1:
			finalstring=finalstring+eachcategory+":"+str(randomconfidence)+"|"
		else:
			finalstring=finalstring+eachcategory+":"+str(randomconfidence)
		eachloopScoreList.remove(randomconfidence)
	detected_objects_withconfidence=finalstring

	_newuploadedvideo = UploadedVideo(filename = filename,extension = extension,storagelocation = storagelocation,detected_objects_withconfidence=detected_objects_withconfidence,uploader_id=random.choice(userids))
	db.session.add(_newuploadedvideo)

db.session.commit()