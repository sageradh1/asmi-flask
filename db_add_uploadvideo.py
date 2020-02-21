from app import app,db
from app.database.models import MergedAdCategory,UploadedVideo
import random

query=MergedAdCategory.query.order_by(MergedAdCategory.id.asc()).limit(10)

allcategories = []
for eachrow in query:
	allcategories.append(eachrow.category_name)

confidenceScoreList = [i for i in range(1,len(allcategories)+1)]

# for index in range(10000):
for index in range(10000):

	filename = "testvideo"+str(index)
	extension = "mp4"
	storagelocation = app.config["VIDEO_UPLOADS_FOLDER"]
	detected_objects_withconfidence=""

	eachloopScoreList =confidenceScoreList.copy()
	

	finalstring=""
	for eachcategory in allcategories:
		randomconfidence= random.choice(eachloopScoreList)

		if len(eachloopScoreList)>1:
			finalstring=finalstring+eachcategory+":"+str(randomconfidence)+","
		else:
			finalstring=finalstring+eachcategory+":"+str(randomconfidence)
		eachloopScoreList.remove(randomconfidence)
	detected_objects_withconfidence=finalstring

	_newuploadedvideo = UploadedVideo(filename = filename,extension = extension,storagelocation = storagelocation,detected_objects_withconfidence=detected_objects_withconfidence)
	db.session.add(_newuploadedvideo)

db.session.commit()