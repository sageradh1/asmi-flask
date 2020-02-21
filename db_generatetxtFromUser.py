from app import db
# from app.database.models import MergedAdCategory,UploadedVideo
from app.database.models import User

query=User.query.order_by(User.id.asc())

f = open("users.txt", "w")
f.write("id,email,username\n")

for eachCategory in query:
	f.write(str(eachCategory.id)+","+eachCategory.email+","+eachCategory.username+"\n")
f.close()