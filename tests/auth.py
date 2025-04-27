import pytest
from app import create_app
from extensions import db
import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库进行测试
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login(client):
    data = {
        "code": "your_test_code"  # 这里需要替换为有效的微信登录 code
    }
    response = client.post('/api/auth/login', json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'token' in result
    assert 'user' in result