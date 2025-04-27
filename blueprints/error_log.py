# blueprints/error_log.py
from flask import Blueprint, request, jsonify
from utils.auth import token_required
from models.error_log import ErrorLog  # 需新增错误日志模型
from extensions import db

error_log_bp = Blueprint('error_log', __name__, url_prefix='/api/errors')

@error_log_bp.route('/', methods=['POST'])
@token_required()
def submit_error_log(current_user):
    data = request.get_json()
    error_log = ErrorLog(
        user_id=current_user.id,
        error_type=data['errorType'],
        description=data['description']
    )
    db.session.add(error_log)
    db.session.commit()
    return jsonify({"message": "错误日志提交成功"}), 200