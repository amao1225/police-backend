from datetime import datetime
from extensions import db

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), unique=True, nullable=False,index=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('open', 'closed'), default='open',index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    officer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "case_number": self.case_number,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }