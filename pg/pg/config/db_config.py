class Config:

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:root@localhost/mobile_shop"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = True