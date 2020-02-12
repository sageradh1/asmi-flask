from app import db
from datetime import datetime



#################reference##############################
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

#################needed##############################
class UploadedVideo(db.Model):
    videoid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True)
    extension = db.Column(db.String(5))
    storagelocation = db.Column(db.String(500))
    uploadStartedTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uploadCompletedTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)    
    detected_objects_withconfidence=db.Column(db.String(1000))

    analyticsFile = db.relationship('VideoAnalyticsFile', backref='videoFile', lazy='dynamic')

    # def __init__(self, name, extension,storagelocation,uploadStartedTime,uploadCompletedTime,analyticsFile):
    #     self.filename = filename
    #     self.extension = extension
    #     self.storagelocation = storagelocation
    #     self.uploadStartedTime = uploadStartedTime
    #     self.uploadCompletedTime = uploadCompletedTime
    #     self.analyticsFile = analyticsFile

    def __repr__(self):
        return "<UploadedVideo filename:{} uploadCompletedTime:{} >".format(self.filename,self.uploadCompletedTime)

class VideoAnalyticsFile(db.Model):
    analyticsfileid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    storagelocation = db.Column(db.String(500))
    createdTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    video_id = db.Column(db.Integer, db.ForeignKey('uploaded_video.videoid'))

    # def __init__(self, filename, storagelocation,createdTime,video_id):
    #     self.filename = filename
    #     self.storagelocation = storagelocation
    #     self.createdTime = createdTime
    #     self.video_id = video_id


    def __repr__(self):
        return '<VideoAnalyticsFile video_id:{}  filename:{} createdTime:{}  >'.format(self.video_id,self.filename,self.createdTime)

class GeneratedVideo(db.Model):
    gvideoid = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    storagelocation = db.Column(db.String(500))
    createdTime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    video_id = db.Column(db.Integer, nullable=False)

    # def __init__(self, filename, storagelocation,createdTime,video_id):
    #     self.filename = filename
    #     self.storagelocation = storagelocation
    #     self.createdTime = createdTime
    #     self.video_id = video_id


    def __repr__(self):
        return '<GeneratedVideo gvideoid:{}  filename:{} createdTime:{} video_id >'.format(self.gvideoid,self.filename,self.createdTime.self.video_id)

class AdCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100),nullable=False)
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<AdCategory adcategoryid:{}  category_name:{} createdTime:{} last_modified_time:{} >'.format(self.id,self.category_name,self.created_time.self.last_modified_time)

class AdPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500),nullable=False)
    brand = db.Column(db.String(200))
    seller = db.Column(db.String(200))
    price = db.Column(db.Numeric(5,2),nullable=False)
    image_url = db.Column(db.String(500),nullable=False)
    intial_quantity = db.Column(db.Integer)
    left_quantity = db.Column(db.Integer)
    created_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    belonging_category = db.Column(db.String(100),nullable=False)


    def __repr__(self):
        return '<AdPost adpostid:{}  title:{} brand:{} video_id >'.format(self.gvideoid,self.filename,self.createdTime.self.video_id)
