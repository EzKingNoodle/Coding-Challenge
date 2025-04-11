# Import required modules
from app import db                                    # Database instance
from datetime import datetime                        # For timestamp handling
from werkzeug.security import generate_password_hash, check_password_hash  # Password security

class User(db.Model):
    __tablename__ = 'users'  # Name of the database table
    
    # Define database columns
    id = db.Column(db.Integer, primary_key=True)     # Unique identifier
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email (must be unique)
    password_hash = db.Column(db.String(255))        # Hashed password
    first_name = db.Column(db.String(80))           # User's first name
    last_name = db.Column(db.String(80))            # User's last name
    is_active = db.Column(db.Boolean, default=True)  # Account status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # Creation timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp
    
    def set_password(self, password):
        # Hash and store password
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        # Verify password against hash
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        # Convert user object to dictionary (for JSON responses)
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }