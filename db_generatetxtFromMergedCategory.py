from app import db
# from app.database.models import MergedAdCategory,UploadedVideo
from app.database.models import MergedAdCategory
import random

query=MergedAdCategory.query.order_by(MergedAdCategory.id.asc())

f = open("app/static/database-asmi/mergedAdCategories.txt", "w")
f.write("cat_id,category_name,adtitle,adprice\n")

for eachCategory in query:
	f.write(str(eachCategory.id)+","+eachCategory.category_name+","+eachCategory.adtitle+","+str(eachCategory.adprice))
	f.write("\n")
f.close()