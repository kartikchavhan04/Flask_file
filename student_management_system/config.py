import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
import os

class Config:

    SECRET_KEY = "student-management-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:Bharat123@localhost/college"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = True