# app/routes/task.py
from flask import Blueprint, request, jsonify
from app.models import db, Task, User
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint('task', __name__, url_prefix='/tasks')

# Create a task
@task_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()

    # Vérifiez si l'utilisateur actuel existe
    current_user = User.query.get(current_user_id)
    if current_user is None:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    new_task = Task(description=data['description'], user=current_user)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

# Read all tasks for the authenticated user
@task_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_tasks():
    current_user_id = get_jwt_identity()

    # Récupérez les paramètres de requête pour la pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))  # Nombre d'éléments par page

    # Calculez l'index de départ et de fin pour la pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Récupérez les tâches pour l'utilisateur actuel dans la plage spécifiée
    tasks = Task.query.filter_by(user_id=current_user_id).slice(start_index, end_index).all()

    # Convertissez les tâches en format JSON
    tasks_data = [{'id': task.id, 'description': task.description} for task in tasks]

    # /tasks?page=1&per_page=5 donnera une page avec cinq tasks
    return jsonify(tasks_data)

# Update a task
@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

# Delete a task
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})
