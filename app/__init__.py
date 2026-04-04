from flask import Flask
from app.services import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret"

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    init_db()
    return app