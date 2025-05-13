import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my-default-secret")  # à personnaliser
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")  # par défaut
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://bankuser:mdp@localhost/bankvision")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]
   
