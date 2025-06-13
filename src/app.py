from flask import Flask
from api.endpoints import home
from config.extensions import db
import os

def create_app():
    app = Flask(__name__)

    # Determine the environment and configure the database URI
    if os.getenv('FLASK_ENV') == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@/{os.getenv('DB_NAME')}?unix_socket=/cloudsql/{os.getenv('INSTANCE_CONNECTION_NAME')}"
        )
    else:
        # Use a local SQLite file for development (more persistent than in-memory)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'

    # Disable track modifications for performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register Blueprints
    app.register_blueprint(home)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
