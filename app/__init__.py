from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

BLACKLIST = set()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=["http://localhost:8080"])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.auth import auth
    from app.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BLACKLIST

    return app
