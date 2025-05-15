from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import BLACKLIST
from . import db
from app.models import User, Account, Transaction


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message="Bienvenue sur BankVision")

@main.route('/login-form')
def login_form():
    return render_template('login.html')

@main.route('/dashboard')
@jwt_required()
def dashboard():
    current_user_identity = get_jwt_identity()

    # Si ton JWT stocke le nom d'utilisateur
    user = User.query.filter_by(username=current_user_identity).first()

    # Sinon, s’il s’agit de l’ID :
    # user = User.query.get(current_user_identity)

    total_users = User.query.count()
    total_accounts = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    total_transactions = Transaction.query.count()

    return render_template('dashboard.html',
                           user=user,
                           total_users=total_users,
                           total_accounts=total_accounts,
                           total_balance=round(total_balance, 2),
                           total_transactions=total_transactions)
