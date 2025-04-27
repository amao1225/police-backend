from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    real_name = db.Column(db.String(50))
    badge_number = db.Column(db.String(20), unique=True)
    role = db.Column(db.String(20), default='officer')
    is_active = db.Column(db.Boolean, default=True)
    
    # 关联关系
    cases = db.relationship('Case', backref='officer', lazy=True)
    tasks = db.relationship('Task', backref='assignee', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)