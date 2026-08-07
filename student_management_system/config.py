import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
import os

class Config:
    SECRET_KEY = "student-management-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "instance", "database.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False