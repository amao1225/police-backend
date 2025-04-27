from datetime import datetime
from extensions import db  # 直接导入根目录的db

class Task(db.Model):  # 继承db.Model
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 新增状态字段（原方案可能遗漏，需与业务接口一致）
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 外键关联用户
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "assignee_id": self.assignee_id,
            "created_at": self.created_at.isoformat()
        }