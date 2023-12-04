# app/routes/user.py
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask import Blueprint, request, jsonify
from app.models import db, User

user_bp = Blueprint('user', __name__, url_prefix='/users')
bcrypt = Bcrypt()

# Renvoie tous les utilisateurs
@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_data)

# Renvoie un utilisateur (id)
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.id, 'username': user.username}
    return jsonify(user_data)

# Mettre à jour les données d'un utilisateur
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    # Vérifier si l'utilisateur authentifié est le même que celui dont l'ID est dans l'URL
    if current_user_id != user_id:
        return jsonify({"message": "Vous n'êtes pas autorisé à effectuer cette action"}), 403

    user = User.query.get_or_404(user_id)
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Nom d'utilisateur ou mot de passe manquant"}), 400

    new_username = data['username']
    new_password = data['password']
    errors = []  # Liste pour stocker les erreurs

    # Vérifier si le nouveau nom d'utilisateur est différent du nom d'utilisateur actuel
    if new_username != user.username:
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            errors.append("Nom d'utilisateur déjà pris")

    # Vérifier la complexité du mot de passe
    if len(new_password) < 4:
        errors.append("Le mot de passe doit contenir au moins 4 caractères")

    if not any(char.isupper() for char in new_password):
        errors.append("Le mot de passe doit contenir au moins une lettre majuscule")

    if not any(char.isdigit() for char in new_password):
        errors.append("Le mot de passe doit contenir au moins un chiffre")

    if not any(char in r"!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in new_password):
        errors.append("Le mot de passe doit contenir au moins un caractère spécial")

    # Si des erreurs sont présentes, les renvoyer
    if errors:
        return jsonify({"errors": errors}), 400

    # Si rien n'a été changé, renvoyer un message approprié
    if new_username == user.username and new_password == user.password:
        return jsonify({'message': "Aucune modification n'a été effectuée"}), 200

    # Sinon, mettre à jour le compte
    user.username = new_username
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Utilisateur mis à jour avec succès'})

# Delete a user
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()

    # Vérifier si l'utilisateur authentifié est le même que celui dont l'ID est dans l'URL
    if current_user_id != user_id:
        return jsonify({"message": "Vous n'êtes pas autorisé à effectuer cette action"}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
