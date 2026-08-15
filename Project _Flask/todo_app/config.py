class Config:

    SECRET_KEY = "your-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:Bharat123@localhost:3306/todo_app"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False