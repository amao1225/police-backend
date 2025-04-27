from flask import Blueprint, request, jsonify
from utils.auth import token_required
from models.case import Case
from extensions import db

case_bp = Blueprint('case', __name__, url_prefix='/api/cases')

@case_bp.route('/', methods=['POST'])
@token_required(roles=['admin', 'officer'])
def create_case(current_user):
    data = request.get_json()
    
    new_case = Case(
        case_number=data['case_number'],
        location=data['location'],
        officer_id=current_user.id
    )
    
    db.session.add(new_case)
    db.session.commit()
    return jsonify(new_case.to_dict()), 201

@case_bp.route('/<int:case_id>', methods=['GET'])
@token_required()
def get_case(current_user, case_id):
    case = Case.query.get_or_404(case_id)
    if current_user.role != 'admin' and case.officer_id != current_user.id:
        return jsonify({'error': '无权访问'}), 403
    
    return jsonify(case.to_dict())