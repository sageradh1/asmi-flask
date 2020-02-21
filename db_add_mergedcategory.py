from app import db,app
from app.database.models import MergedAdCategory
import random


####################Generate input for MergedCategory###############
listofOurCategories = ["Shirt","Trousers","Footwear","Handbag","Watch","Guitar","Mobile_phone","Headphones","Hat","Sunglasses"]
counter=1
for eachlable in listofOurCategories:
	category_name = eachlable
	doesExist = MergedAdCategory.query.filter_by(category_name=category_name).scalar() is not None
	if doesExist:
		print(category_name+" already present in the database")
		continue

	adtitle = "Ad for "+category_name
	adbrand = category_name+ "Brand"
	adseller = "Seller"+str(counter)
	counter=counter+1
	adprice = random.randrange(0,100)
	adimage_url = app.config["ADIMAGE_UPLOADS_FOLDER"]+"/testimage.jpg"
	adinitial_quantity = random.randrange(10000, 20000)
	adleft_quantity = adinitial_quantity

	_merged_category = MergedAdCategory(category_name=category_name,adtitle=adtitle,adbrand=adbrand,adseller=adseller,adprice=adprice,adimage_url=adimage_url,adinitial_quantity=adinitial_quantity,adleft_quantity=adleft_quantity)
	db.session.add(_merged_category)

db.session.commit()
####################Generate input for MergedCategory###############
