import os

SECRET_KEY = 'secret-key'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2171_exam:@std-mysql.ist.mospolytech.ru/std_2171_exam'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

ADMINROLE_ID=1
MODERROLE_ID=2
USERROLE_ID=3
UNWATCHED_REVIEW_STAT_ID=1
BOOKS_PER_PAGE = 6
REVIEWS_PER_PAGE = 2

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
