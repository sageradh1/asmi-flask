import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    DEBUG = False
    TESTING = False
    generateSecretKey= secrets.token_hex(16)
    #SECRET_KEY = secrets.token_urlsafe(16)
    SECRET_KEY = generateSecretKey
    #print("The generated new Secret key is "+generateSecretKey)
    #print("The base url is {}".format(basedir))

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/uploaded"
    CSV_UPLOADS_FOLDER =  basedir+"/app/static/csv/uploaded"
    VIDEO_UPLOADS_FOLDER =  basedir+"/app/static/video/uploaded"
    VIDEO_GENERATED_FOLDER =  basedir+"/app/static/video/generated"
    VIDEOANALYTICS_GENERATED_FOLDER =  basedir+"/app/static/analyticsFolder/generated"
    
    MAX_VIDEO_FILESIZE = 16 * 1024 * 1024 #max allowed video filesize is 16MB
    MAX_CSV_FILESIZE = 10 * 1024 * 1024 #max allowed csv filesize is 10MB

    ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'mkv'])
    ALLOWED_USERDATA_EXTENSIONS = set(['csv'])

    SESSION_COOKIE_SECURE = True
    
class DevelopmentConfig(Config):
    DEBUG = True
    
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql://asmi_group:asmipassword123@localhost/asmi_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_NAME = "asmi_db"
    DB_USERNAME = "asmi_group"
    DB_PASSWORD = "asmipassword123"

    IMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/uploaded"
    CSV_UPLOADS_FOLDER =  basedir+"/app/static/csv/uploaded"
    VIDEO_UPLOADS_FOLDER =  basedir+"/app/static/video/uploaded"
    VIDEO_GENERATED_FOLDER =  basedir+"/app/static/video/generated"
    VIDEOANALYTICS_GENERATED_FOLDER =  basedir+"/app/static/analyticsFolder/generated"

    SESSION_COOKIE_SECURE = False

    

class TestingConfig(Config):
    TESTING = True
    DB_NAME = "testing-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    IMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/uploaded"
    CSV_UPLOADS_FOLDER =  basedir+"/app/static/csv/uploaded"
    VIDEO_UPLOADS_FOLDER =  basedir+"/app/static/video/uploaded"
    
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass
