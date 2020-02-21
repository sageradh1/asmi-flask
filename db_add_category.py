from app import db
from app.database.models import AdCategory

listofOurCategories = ["Shirt","Trousers","Footwear","Handbag","Watch","Guitar","Mobile_phone","Headphones","Hat","Sunglasses"]
for eachlable in listofOurCategories:
	category_name = eachlable
	doesExist = AdCategory.query.filter_by(category_name=category_name).scalar() is not None
	if doesExist:
		print(category_name+" already present in the database")
		continue

	_category = AdCategory(category_name=category_name)
	db.session.add(_category)
db.session.commit()
