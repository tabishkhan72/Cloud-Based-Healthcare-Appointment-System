from flask import Flask,Blueprint
from api.endpoints import *
from flask_sqlalchemy import SQLAlchemy
from models.models import *
from config.extensions import db
from api.endpoints import home
import os



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' #For local testing
    

    if os.getenv('FLASK_ENV') == 'production':
        # Use production database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<INSTANCE_CONNECTION_NAME>'
    else:
        # Use local database for development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(home)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)