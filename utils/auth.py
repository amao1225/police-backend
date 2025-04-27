import jwt
from functools import wraps
from flask import request, jsonify, current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from models.user import User

def token_required(roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            
            if not token:
                return jsonify({
                    'code': 401,
                    'message': '缺少访问令牌'
                }), 401

            try:
                payload = jwt.decode(
                    token, 
                    current_app.config['SECRET_KEY'],
                    algorithms=[current_app.config['JWT_ALGORITHM']]
                )
                current_user = User.query.get(payload['user_id'])
                
                if not current_user or not current_user.is_active:
                    raise InvalidTokenError("用户无效")
                
                if roles and current_user.role not in roles:
                    return jsonify({
                        'code': 403,
                        'message': '权限不足'
                    }), 403
                    
            except ExpiredSignatureError:
                return jsonify({
                    'code': 401,
                    'message': '令牌已过期'
                }), 401
            except InvalidTokenError:
                return jsonify({
                    'code': 401,
                    'message': '无效令牌'
                }), 401
                
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator