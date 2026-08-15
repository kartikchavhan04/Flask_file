from flask import Flask

from config import Config
from app.extensions import db




def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.models import User,Task


    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    return app