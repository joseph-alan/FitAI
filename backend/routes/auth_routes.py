from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "gender": "male"
    }
    """
    try:
        # Check if request has JSON content
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        # Parse JSON with error handling
        try:
            data = request.get_json()
        except Exception as json_error:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        response_data, status_code = AuthService.register_user(data)
        return jsonify(response_data), status_code
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT tokens.
    
    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        # Check if request has JSON content
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        # Parse JSON with error handling
        try:
            data = request.get_json()
        except Exception as json_error:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        response_data, status_code = AuthService.login_user(data)
        return jsonify(response_data), status_code
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile.
    Requires valid JWT token in Authorization header.
    """
    try:
        current_user_id = get_jwt_identity()
        user = AuthService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile retrieved successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.
    Requires valid refresh token in Authorization header.
    """
    try:
        from flask_jwt_extended import create_access_token
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'message': 'Token refreshed successfully',
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 