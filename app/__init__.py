from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# 🔒 Liste noire pour les tokens JWT révoqués
BLACKLIST = set()

# Importation du blueprint 'auth' depuis le fichier 'auth.py'
from .auth import auth  # Assure-toi de cette ligne

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enregistrement des blueprints
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(auth)  # Assure-toi d'enregistrer 'auth'

    return app

# 🔁 Vérifie si le token est dans la blacklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST
