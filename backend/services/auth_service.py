from typing import Optional, Tuple
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User, db
from schemas.user_schema import UserRegistrationSchema, UserLoginSchema
from marshmallow import ValidationError

class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def register_user(user_data: dict) -> Tuple[dict, int]:
        """
        Register a new user.
        
        Args:
            user_data: Dictionary containing user registration data
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Validate input data
            schema = UserRegistrationSchema()
            validated_data = schema.load(user_data)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=validated_data['email']).first()
            if existing_user:
                return {'error': 'User with this email already exists'}, 409
            
            # Create new user
            user = User(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                date_of_birth=validated_data['date_of_birth'],
                gender=validated_data['gender']
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Generate tokens
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return {
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 201
            
        except ValidationError as e:
            return {'error': 'Validation error', 'details': e.messages}, 400
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def login_user(login_data: dict) -> Tuple[dict, int]:
        """
        Authenticate user and generate tokens.
        
        Args:
            login_data: Dictionary containing login credentials
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Validate input data
            schema = UserLoginSchema()
            validated_data = schema.load(login_data)
            
            # Find user by email
            user = User.query.filter_by(email=validated_data['email']).first()
            if not user:
                return {'error': 'Invalid email or password'}, 401
            
            # Check if user is active
            if not user.is_active:
                return {'error': 'Account is deactivated'}, 401
            
            # Verify password
            if not user.check_password(validated_data['password']):
                return {'error': 'Invalid email or password'}, 401
            
            # Generate tokens
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            return {
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
            
        except ValidationError as e:
            return {'error': 'Validation error', 'details': e.messages}, 400
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return {'error': 'Internal server error'}, 500
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID as string
            
        Returns:
            User object or None
        """
        try:
            return User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(f"Error getting user by ID: {str(e)}")
            return None 