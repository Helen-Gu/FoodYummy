import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    
    FY_MAIL_SUBJECT_PREFIX = 'Dear User: '
    FY_MAIL_SENDER = '[FoodYummy] <duoduo.liu@mail.mcgill.com>'
    FY_ADMIN = 'foodyummy307@gmail.com'
    UPLOAD_FOLDER = './user'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    UPLOAD_FOLDER_DISH= os.path.join(basedir,"app/static/images/dish")
    UPLOAD_FOLDER_RECIPE =  os.path.join(basedir,"app/static/images/recipe")
    UPLOAD_FOLDER_USER = os.path.join(basedir,"app/static/user")
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'foodyummy307@gmail.com'
    MAIL_PASSWORD = 'comp307Proj'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MONGO_URI = 'mongodb://localhost:27017/FoodYummy'
    MONGODB_DB = 'FoodYummy'

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongomock://localhost:27017/testdb'

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'default': DevelopmentConfig
}
