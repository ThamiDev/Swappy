# run.py
from app import app, db, models

def init_db():
    try:
        with app.app_context():
            db.create_all()
            print('Lancement de la base de données !')
    except Exception as e:
        print(f"Une erreur s'est produite lors du lancement de la base de données : {e}")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
