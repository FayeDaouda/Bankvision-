from app import create_app

app = create_app()

if __name__ == '__main__':
    # Définir le port à 8080
    app.run(debug=True, port=8080)
