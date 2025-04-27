import pytest
from models.user import User
from extensions import db

@pytest.fixture
def app():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库

    with app.app_context():
        db.create_all()  # 创建表结构
        yield app
        db.drop_all()     # 清理数据库

def test_user_model(app):
    with app.app_context():
        # 1. 创建用户并设置密码（业务逻辑：必须设置密码）
        user = User(username="test_user")
        user.set_password("test_password")  # 生成 password_hash

        # 2. 提交到数据库（触发数据库默认值和非空约束）
        db.session.add(user)
        db.session.commit()

        # 3. 从数据库查询用户（使用 Session.get() 消除警告）
        db_user = db.session.get(User, user.id)  # 替代 User.query.get()

        # 4. 断言验证（验证数据库中的值，而非实例属性）
        assert db_user.check_password("test_password") is True  # 密码验证通过
        assert db_user.role == "officer"  # 数据库默认值生效（不再是 None）
        assert db_user.password_hash is not None  # 非空约束通过    