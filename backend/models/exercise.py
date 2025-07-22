from flask_sqlalchemy import SQLAlchemy
from models.user import db

class Exercise(db.Model):
    """Exercise model for workout exercises."""
    
    __tablename__ = 'exercises'
    
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    equipment = db.Column(db.Text)
    instructions = db.Column(db.Text)
    images = db.Column(db.ARRAY(db.Text))
    primary_muscles = db.Column(db.ARRAY(db.Text))
    secondary_muscles = db.Column(db.ARRAY(db.Text))
    
    def to_dict(self) -> dict:
        """Convert exercise object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'equipment': self.equipment,
            'instructions': self.instructions,
            'images': self.images,
            'primary_muscles': self.primary_muscles,
            'secondary_muscles': self.secondary_muscles
        }
    
    def __repr__(self):
        return f'<Exercise {self.name}>' 