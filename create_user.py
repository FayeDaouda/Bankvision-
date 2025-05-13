# create_user.py
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User(
        username="admin",
        email="admin@example.com",
        password=generate_password_hash("admin123")
    )
    db.session.add(user)
    db.session.commit()
    print("Utilisateur créé avec succès")
