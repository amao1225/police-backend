from flask import Blueprint, request, jsonify
from utils.auth import token_required
from models.task import Task
from extensions import db

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')

@task_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def create_task(current_user):
    data = request.get_json()
    
    new_task = Task(
        title=data['title'],
        content=data['content'],
        assignee_id=data['assignee_id']
    )
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
@token_required()
def update_task_status(current_user, task_id):
    task = Task.query.get_or_404(task_id)
    
    if current_user.id != task.assignee_id and current_user.role != 'admin':
        return jsonify({'error': '无权操作'}), 403
    
    task.status = request.json.get('status', task.status)
    db.session.commit()
    return jsonify(task.to_dict())