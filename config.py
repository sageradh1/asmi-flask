import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#comment here also jabir
# from loadpandasdf import loadvideofeaturesdf_videoiddf

# classes = ["Shirt","Trousers","Footwear","Handbag","Watch","Guitar","Mobile_phone","Headphones","Hat","Sunglasses"]

class Config(object):
    DEBUG = False
    TESTING = False


    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ['sageradh@gmail.com']
    
    # generateSecretKey= secrets.token_hex(16)
    # #SECRET_KEY = secrets.token_urlsafe(16)
    # SECRET_KEY = generateSecretKey
    #print("The generated new Secret key is "+generateSecretKey)
    #print("The base url is {}".format(basedir))

    
    #comment here jabir
    # VIDEO_WITH_FEATURES_DF, MATRIX_WITH_VIDEOID,USERVIEWNORMALISEDDF = loadvideofeaturesdf_videoiddf()
    
    # #asmidf
    # print("asmidf")
    # print(MATRIX_WITH_VIDEOID)
    # #newdf
    # print("newdf")
    # print(VIDEO_WITH_FEATURES_DF)
    # # normaliseddf
    # print("normaliseddf")
    # print(USERVIEWNORMALISEDDF)
    
    ADIMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/uploaded/adimages"
    IMAGE_UPLOADS_FOLDER = basedir+ "/app/static/img/uploaded"
    CSV_UPLOADS_FOLDER =  basedir+"/app/static/csv/uploaded"
    VIDEO_UPLOADS_FOLDER =  basedir+"/app/static/video/uploaded"
    VIDEO_GENERATED_FOLDER =  basedir+"/app/static/video/generated"
    VIDEOANALYTICS_GENERATED_FOLDER =  basedir+"/app/static/analyticsFolder/generated"
    
    MAX_VIDEO_FILESIZE = 50 * 1024 * 1024 #max allowed video filesize is 16MB
    MAX_CSV_FILESIZE = 10 * 1024 * 1024 #max allowed csv filesize is 10MB

    ALLOWED_VIDEO_EXTENSIONS = set(['mp4', 'mkv'])
    ALLOWED_USERDATA_EXTENSIONS = set(['csv'])

    SESSION_COOKIE_SECURE = True

    SECRET_KEY = os.getenv('WEBAPP_SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    
    # SQLALCHEMY_DATABASE_URI = "postgresql://asmi_group:asmipassword123@localhost/asmi_db"
    
    # SQLALCHEMY_DATABASE_URI = "postgresql://asmi_group:asmipassword123@localhost/asmi_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_NAME = os.getenv('DEV_DB_NAME')
    DB_USERNAME = os.getenv('DEV_DB_USERNAME')
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')

    SESSION_COOKIE_SECURE = False

    STRIPE_SECRET_KEY =os.getenv("DEV_STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY =os.getenv("DEV_STRIPE_PUBLISHABLE_KEY")

class TestingConfig(Config):
    TESTING = True

    DB_NAME = os.getenv('TEST_DB_NAME')
    DB_USERNAME = os.getenv('TEST_DB_USERNAME')
    DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')


    SESSION_COOKIE_SECURE = False
    STRIPE_SECRET_KEY =os.getenv("TEST_STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY =os.getenv("TEST_STRIPE_PUBLISHABLE_KEY")

class ProductionConfig(Config):
    pass