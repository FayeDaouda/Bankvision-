from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app import db
from flask import render_template
from app.models import User

auth = Blueprint('auth', __name__)



