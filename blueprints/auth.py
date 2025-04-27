from flask import Blueprint, request, jsonify
import datetime
import jwt
import requests
from models.user import User
from extensions import db
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({
            'code': 400,
            'message': '缺少微信登录 code'
        }), 400

    # 使用 code 换取 session_key 和 openid
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={Config.WX_APPID}&secret={Config.WX_SECRET}&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    res_data = response.json()
    openid = res_data.get('openid')
    session_key = res_data.get('session_key')
    if not openid or not session_key:
        return jsonify({
            'code': 401,
            'message': '微信登录失败'
        }), 401

    # 根据 openid 查找用户，如果不存在则创建新用户
    user = User.query.filter_by(username=openid).first()
    if not user:
        user = User(username=openid)
        db.session.add(user)
        db.session.commit()

    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_EXPIRATION)
    }, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role
        }
    })