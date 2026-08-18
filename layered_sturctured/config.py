class Config:

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:password@localhost/employee_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False