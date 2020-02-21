from app import app,db
from app.database.models import User
from app.utils.hashpassword import hash_password
import random

emailList = ["testemail1@domain.com","testemail2@domain.com"]
usernameList = ["user1","user2"]
password_hashList = [hash_password("password"),hash_password("password")]

#range(2) means from index 0 to 1
for index in range(2):
	email = emailList[index]
	username = usernameList[index]
	password_hash =password_hashList[index]

	_newuser = User(email=email,username=username,password_hash=password_hash)
	db.session.add(_newuser)

db.session.commit()