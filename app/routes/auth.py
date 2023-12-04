from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import db, User
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Vérifier si il y a l'username ainsi que le mot de passe
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe manquant"}), 400

    username = data['username']
    password = data['password']
    errors = []  # Liste pour stocker les erreurs

    # Vérifier si l'utilisateur existe déjà
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        errors.append("Nom d'utilisateur déjà pris")

    # Vérifier la complexité du mot de passe
    if len(password) < 4:
        errors.append("Le mot de passe doit contenir au moins 4 caractères")

    if not any(char.isupper() for char in password):
        errors.append("Le mot de passe doit contenir au moins une lettre majuscule")

    if not any(char.isdigit() for char in password):
        errors.append("Le mot de passe doit contenir au moins un chiffre")

    if not any(char in r"!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password):
        errors.append("Le mot de passe doit contenir au moins un caractère spécial")

    # Si des erreurs sont présentes, les renvoyer
    if errors:
        return jsonify({"errors": errors}), 400

    # Sinon, créer un nouvel utilisateur
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    # Vérifier si il y a l'username ainsi que le mot de passe
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe manquant"}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(username=user.username, id=user.id), 200