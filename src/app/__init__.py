from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(config_filename=None):
    app = Flask(__name__)

    # Load configuration
    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object('config.Config')

    # Import and register blueprint from routes
    from app.routes import main_bp
    app.register_blueprint(main_bp, url_prefix=os.environ.get('PREFIX'))

    return app