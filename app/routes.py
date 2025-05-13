from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt
from app import BLACKLIST
from . import db
from app.models import User


main = Blueprint('main', __name__)

# Utilisateur fictif (simuler un utilisateur en base de données)
fake_user = {
    "username": "admin",
    "password_hash": generate_password_hash("admin123")  # Tu peux l'imprimer si besoin
}

@main.route('/')
def home():
    return jsonify(message="Bienvenue sur BankVision")

# Page de connexion (formulaire HTML)
@main.route('/login-form')
def login_form():
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    return "<h1>Bienvenue sur votre tableau de bord BankVision 🏦</h1>"


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Champs manquants"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200


# La route signup a été déplacée dans 'auth.py', donc on la supprime ici
# @main.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     if User.query.filter_by(username=username).first():
#         return jsonify(msg="Nom d'utilisateur déjà pris"), 400

#     hashed_pw = generate_password_hash(password)
#     new_user = User(username=username, email=email, password=hashed_pw)

#     from app import db
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify(msg="Utilisateur enregistré avec succès"), 201

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify(msg="Nom d'utilisateur déjà pris"), 400

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(msg="Utilisateur enregistré avec succès"), 201

    # Si GET, on affiche le formulaire HTML
    return render_template('signup.html')


@main.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLACKLIST.add(jti)
    return jsonify(msg="Déconnexion réussie"), 200
