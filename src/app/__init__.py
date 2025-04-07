from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprint from routes
    from app.routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/auth")

    return app