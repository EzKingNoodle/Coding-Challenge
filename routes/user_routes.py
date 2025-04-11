# Import required modules
from flask import Blueprint, request, jsonify           # Flask components
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity  # JWT functions
from models.user import User                           # User model
from app import db                                     # Database instance
from marshmallow import Schema, fields, validate, ValidationError  # Data validation
from werkzeug.exceptions import NotFound               # Error handling

# Create blueprint for user routes
user_bp = Blueprint('user', __name__)

# Define data validation schema
class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))  # Username validation
    email = fields.Email(required=True)                # Email validation
    password = fields.Str(required=True, validate=validate.Length(min=6))  # Password validation
    first_name = fields.Str()                         # Optional first name
    last_name = fields.Str()                          # Optional last name

user_schema = UserSchema()  # Create schema instance

# Handle 404 errors
@user_bp.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

# Registration endpoint
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        # Validate input data
        data = user_schema.load(request.get_json())
        
        # Check for duplicate username
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
            
        # Check for duplicate email
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        user.set_password(data['password'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return jsonify(user.to_dict()), 201
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

# Login endpoint
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    # Verify credentials and create token
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
        
    return jsonify({'error': 'Invalid credentials'}), 401

# Get current user endpoint
@user_bp.route('/me', methods=['GET'])
@jwt_required()  # Requires valid JWT token
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Get specific user endpoint
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

# Update user endpoint
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # Check authorization
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    data = request.get_json()
    
    # Update username if provided
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
        
    # Update email if provided
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
        
    # Update password if provided
    if 'password' in data:
        user.set_password(data['password'])
        
    # Update first name if provided
    if 'first_name' in data:
        user.first_name = data['first_name']
        
    # Update last name if provided
    if 'last_name' in data:
        user.last_name = data['last_name']
        
    db.session.commit()
    return jsonify(user.to_dict())

# Delete user endpoint
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Check authorization
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    # Delete user from database
    db.session.delete(user)
    db.session.commit()
    return '', 204