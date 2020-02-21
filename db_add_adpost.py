from app import app,db
from app.database.models import AdCategory,AdPost
import random

query=AdCategory.query.order_by(AdCategory.id.desc()).limit(10)

allcategories = []
for eachcategory in query:
	allcategories.append(eachcategory.category_name)

# print(allcategories)

for index in range(10000):
	title = "Adtitle" + str(index)
	brand = "Brand"+str(index)
	seller = "Seller"+str(index)
	price = random.randrange(0,20)
	# image_url = "18.221.137.201/app/static/video/uploaded/"
	image_url = app.config["ADIMAGE_UPLOADS_FOLDER"]+"/testimage.jpg"
	initial_quantity = random.randrange(10000, 20000)
	left_quantity = initial_quantity
	belonging_category_id = random.randrange(1,10)
	_newpost = AdPost(title=title,brand=brand,seller=seller,price=price,image_url=image_url,initial_quantity=initial_quantity,left_quantity=left_quantity,belonging_category_id=belonging_category_id)
	db.session.add(_newpost)

db.session.commit()

# for eachcategory in query:
# 	print(eachcategory)