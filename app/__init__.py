from flask import Flask
from flask_cors import CORS
from app.routes.newsletter import newsletter_bp
from app.routes.index import index_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registrar blueprints
    app.register_blueprint(newsletter_bp)
    app.register_blueprint(index_bp)

    return app
