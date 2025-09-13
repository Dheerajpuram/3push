from db import db
from datetime import datetime

class Usage(db.Model):
    __tablename__ = 'usage'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    usage_date = db.Column(db.Date, nullable=False)
    data_used_gb = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'usage_date': self.usage_date.isoformat() if self.usage_date else None,
            'data_used_gb': float(self.data_used_gb),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
