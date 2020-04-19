from app import app,db
from app.database.models import User,Profile

allUsersList=User.query.all()
# allUsersList=User.query.order_by(User.videoid.desc()).limit(5)
for eachUser in allUsersList:
#     print(video.detected_objects_withconfidence)
	doesProfileExist = Profile.query.filter_by(user_id=eachUser.id).scalar()
	if doesProfileExist is None:
		try:
			itsprofile = Profile(
				login_email=eachUser.email,
				user_id=eachUser.id
				)
			db.session.add(itsprofile)
		except Exception as err:
			print()

db.session.commit()


# for index in range(2):
# 	email = emailList[index]
# 	username = usernameList[index]
# 	password_hash =password_hashList[index]

# 	_newuser = User(email=email,username=username,password_hash=password_hash)
# 	db.session.add(_newuser)

# db.session.commit()