# models/task.py
from database import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pendente', nullable=False)
    due_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    
    # Chave Estrangeira: user_id (Requisito de associação)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)