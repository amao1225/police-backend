import pytest
from models.user import User
from extensions import db


@pytest.fixture
def app():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_user_model(app):
    with app.app_context():
        # 创建用户并设置密码
        user = User(username="test_user")
        user.set_password("test_password")

        # 将用户实例添加到数据库会话并提交事务
        db.session.add(user)
        db.session.commit()

        # 从数据库中重新查询用户实例
        db_user = db.session.get(User, user.id)

        # 对从数据库查询出的用户实例进行断言
        assert db_user.check_password("test_password") is True
        assert db_user.role == "officer"