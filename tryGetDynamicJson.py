from app import app
from app.database.models import MergedAdCategory
import json

def dynamicJsonFile(_filename,requiredObjectLabels):
	#Extract all the required informations such as image urls, prices, etc from MergedAdCategory
	infoForAllLabelsList=[]
	for j in range(len(requiredObjectLabels)):
		try:
			mergedAd =  MergedAdCategory.query.filter_by(category_name=requiredObjectLabels[j]).first()
			allinfoForThisCategory={}
			if mergedAd is None:
				allinfoForThisCategory['category_name']=requiredObjectLabels[j]
				allinfoForThisCategory['adimage_url']="No information"
				allinfoForThisCategory['price']="No information"
			else:
				allinfoForThisCategory['category_name']=requiredObjectLabels[j]
				allinfoForThisCategory['adimage_url']=str(mergedAd.adimage_url)
				allinfoForThisCategory['price']=str(mergedAd.adprice)

			infoForAllLabelsList.append(allinfoForThisCategory.copy())
		except Exception as err:
			print("Problem while extracting information from Merged Ad Category Table")
			print(err)

	# print(infoForAllLabelsList)

	with open(app.config["VIDEOANALYTICS_GENERATED_FOLDER"]+"/"+_filename, 'r') as f:
	    # print("Extracting data from file")
	    data = json.load(f)
	f.close()

	olddataPerTimestamp = data['dataPerTimestamp']
	newdataPerTimestamp = []

	for i in range(len(olddataPerTimestamp)):

		eachdict_For_newdataPerTimestamp = {}	
		eachdict_For_newdataPerTimestamp['timeInMilliSec']=olddataPerTimestamp[i]['timeInMilliSec']
		
		allobjects = olddataPerTimestamp[i]['objectsWithCoordinates']
		eachdict_For_newdataPerTimestamp['objectsWithCoordinates']=[]
		for a in range(len(allobjects)):
			currentobjectwithcoordinate = allobjects[a]
			if currentobjectwithcoordinate["label"] in requiredObjectLabels:
				currentobjectwithcoordinate['adimage_url']=infoForAllLabelsList[requiredObjectLabels.index(currentobjectwithcoordinate["label"])]['adimage_url']
				currentobjectwithcoordinate['price']=infoForAllLabelsList[requiredObjectLabels.index(currentobjectwithcoordinate["label"])]['price']

				eachdict_For_newdataPerTimestamp['objectsWithCoordinates'].append(currentobjectwithcoordinate.copy())

		newdataPerTimestamp.append(eachdict_For_newdataPerTimestamp.copy())

	# print(newdataPerTimestamp)
	return newdataPerTimestamp