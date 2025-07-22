from flask_restx import Api, Resource, fields, Namespace
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService
from models.user import User

# Create API documentation
api = Api(
    title='Workout API',
    version='1.0',
    description='A comprehensive API for workout management with user authentication',
    doc='/docs',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type "Bearer" followed by a space and JWT token'
        }
    },
    security='Bearer Auth'
)

# Create namespaces
auth_ns = Namespace('auth', description='Authentication operations')
exercise_ns = Namespace('exercises', description='Exercise operations')

# Define models for Swagger documentation
user_registration_model = api.model('UserRegistration', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password (min 6 characters)', example='password123'),
    'first_name': fields.String(required=True, description='User first name', example='John'),
    'last_name': fields.String(required=True, description='User last name', example='Doe'),
    'date_of_birth': fields.Date(required=True, description='User date of birth (YYYY-MM-DD)', example='1990-01-01'),
    'gender': fields.String(required=True, description='User gender', enum=['male', 'female', 'other'], example='male')
})

user_login_model = api.model('UserLogin', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'password': fields.String(required=True, description='User password', example='password123')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'date_of_birth': fields.Date(description='User date of birth'),
    'gender': fields.String(description='User gender'),
    'created_at': fields.DateTime(description='Account creation date'),
    'updated_at': fields.DateTime(description='Last update date'),
    'is_active': fields.Boolean(description='Account status')
})

auth_response_model = api.model('AuthResponse', {
    'message': fields.String(description='Response message'),
    'user': fields.Nested(user_response_model, description='User information'),
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.Raw(description='Error details (optional)')
})

success_model = api.model('Success', {
    'message': fields.String(description='Success message'),
    'user': fields.Nested(user_response_model, description='User information')
})

token_refresh_model = api.model('TokenRefresh', {
    'message': fields.String(description='Success message'),
    'access_token': fields.String(description='New JWT access token')
})

health_model = api.model('Health', {
    'status': fields.String(description='API status'),
    'message': fields.String(description='Status message')
})

# Exercise models
exercise_model = api.model('Exercise', {
    'id': fields.String(description='Exercise ID'),
    'name': fields.String(description='Exercise name'),
    'equipment': fields.String(description='Equipment needed'),
    'instructions': fields.String(description='Exercise instructions'),
    'images': fields.List(fields.String, description='Exercise images'),
    'primary_muscles': fields.List(fields.String, description='Primary muscle groups'),
    'secondary_muscles': fields.List(fields.String, description='Secondary muscle groups')
})

exercises_grouped_model = api.model('ExercisesGrouped', {
    'message': fields.String(description='Response message'),
    'exercises': fields.Raw(description='Exercises grouped by muscle groups'),
    'total_muscle_groups': fields.Integer(description='Total number of muscle groups'),
    'total_exercises': fields.Integer(description='Total number of exercises')
})

muscle_groups_model = api.model('MuscleGroups', {
    'message': fields.String(description='Response message'),
    'muscle_groups': fields.List(fields.String, description='Available muscle groups'),
    'count': fields.Integer(description='Number of muscle groups')
})

exercises_by_muscle_model = api.model('ExercisesByMuscle', {
    'message': fields.String(description='Response message'),
    'muscle_group': fields.String(description='Requested muscle group'),
    'exercises': fields.List(fields.Nested(exercise_model), description='Exercises for the muscle group'),
    'count': fields.Integer(description='Number of exercises')
})

# Add namespaces to API
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(exercise_ns, path='/api/exercises')

@auth_ns.route('/register')
class UserRegistration(Resource):
    @auth_ns.expect(user_registration_model)
    @auth_ns.response(201, 'User registered successfully', auth_response_model)
    @auth_ns.response(400, 'Validation error or invalid JSON', error_model)
    @auth_ns.response(409, 'User already exists', error_model)
    @auth_ns.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Register a new user
        
        This endpoint allows users to create a new account with their personal information.
        The password will be securely hashed using bcrypt.
        
        **Required Fields:**
        - email: Valid email address
        - password: Minimum 6 characters
        - first_name: User's first name
        - last_name: User's last name
        - date_of_birth: Date in YYYY-MM-DD format
        - gender: One of 'male', 'female', or 'other'
        
        **Returns:**
        - User information
        - JWT access token (valid for 1 hour)
        - JWT refresh token (valid for 30 days)
        """
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            response_data, status_code = AuthService.register_user(data)
            return response_data, status_code
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(user_login_model)
    @auth_ns.response(200, 'Login successful', auth_response_model)
    @auth_ns.response(400, 'Validation error or invalid JSON', error_model)
    @auth_ns.response(401, 'Invalid credentials', error_model)
    @auth_ns.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Authenticate user and get JWT tokens
        
        This endpoint authenticates users with their email and password,
        returning JWT tokens for subsequent API access.
        
        **Required Fields:**
        - email: User's registered email address
        - password: User's password
        
        **Returns:**
        - User information
        - JWT access token (valid for 1 hour)
        - JWT refresh token (valid for 30 days)
        """
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            response_data, status_code = AuthService.login_user(data)
            return response_data, status_code
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@auth_ns.route('/profile')
class UserProfile(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @auth_ns.response(200, 'Profile retrieved successfully', success_model)
    @auth_ns.response(401, 'Unauthorized', error_model)
    @auth_ns.response(404, 'User not found', error_model)
    @auth_ns.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get current user profile
        
        This endpoint returns the profile information of the currently authenticated user.
        Requires a valid JWT access token in the Authorization header.
        
        **Headers:**
        - Authorization: Bearer <access_token>
        
        **Returns:**
        - Current user's profile information
        """
        try:
            current_user_id = get_jwt_identity()
            user = AuthService.get_user_by_id(current_user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'message': 'Profile retrieved successfully',
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@auth_ns.route('/refresh')
class TokenRefresh(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @auth_ns.response(200, 'Token refreshed successfully', token_refresh_model)
    @auth_ns.response(401, 'Invalid refresh token', error_model)
    @auth_ns.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Refresh access token
        
        This endpoint allows users to get a new access token using their refresh token.
        The refresh token should be provided in the Authorization header.
        
        **Headers:**
        - Authorization: Bearer <refresh_token>
        
        **Returns:**
        - New JWT access token (valid for 1 hour)
        """
        try:
            from flask_jwt_extended import create_access_token
            current_user_id = get_jwt_identity()
            new_access_token = create_access_token(identity=current_user_id)
            
            return {
                'message': 'Token refreshed successfully',
                'access_token': new_access_token
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

# Health check endpoint
@api.route('/health')
class HealthCheck(Resource):
    @api.response(200, 'API is healthy', health_model)
    def get(self):
        """
        Health check endpoint
        
        This endpoint provides a simple health check for the API.
        Useful for monitoring and load balancers.
        
        **Returns:**
        - API status and message
        """
        return {
            'status': 'healthy',
            'message': 'Workout API is running'
        }, 200

# Exercise endpoints
@exercise_ns.route('/grouped')
class ExercisesGrouped(Resource):
    @exercise_ns.doc(security='Bearer Auth')
    @exercise_ns.response(200, 'Exercises retrieved successfully', exercises_grouped_model)
    @exercise_ns.response(401, 'Unauthorized', error_model)
    @exercise_ns.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all exercises grouped by primary muscles
        
        This endpoint fetches all exercises from the database and groups them
        by the first muscle in the primary_muscles array. Only authenticated users
        can access this endpoint.
        
        **Headers:**
        - Authorization: Bearer <access_token>
        
        **Returns:**
        - Dictionary with muscle groups as keys and lists of exercises as values
        - Total count of muscle groups and exercises
        """
        try:
            from services.exercise_service import ExerciseService
            response_data, status_code = ExerciseService.get_exercises_grouped_by_primary_muscles()
            return response_data, status_code
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@exercise_ns.route('/muscle-groups')
class MuscleGroups(Resource):
    @exercise_ns.doc(security='Bearer Auth')
    @exercise_ns.response(200, 'Muscle groups retrieved successfully', muscle_groups_model)
    @exercise_ns.response(401, 'Unauthorized', error_model)
    @exercise_ns.response(500, 'Internal server error', error_model)
    def get(self):
        """
        Get all available muscle groups
        
        This endpoint returns a list of all unique muscle groups available
        in the exercises database. Only authenticated users can access this endpoint.
        
        **Headers:**
        - Authorization: Bearer <access_token>
        
        **Returns:**
        - List of available muscle groups
        - Count of muscle groups
        """
        try:
            from services.exercise_service import ExerciseService
            response_data, status_code = ExerciseService.get_available_muscle_groups()
            return response_data, status_code
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@exercise_ns.route('/muscle-group/<muscle_group>')
class ExercisesByMuscleGroup(Resource):
    @exercise_ns.doc(security='Bearer Auth')
    @exercise_ns.response(200, 'Exercises retrieved successfully', exercises_by_muscle_model)
    @exercise_ns.response(401, 'Unauthorized', error_model)
    @exercise_ns.response(500, 'Internal server error', error_model)
    def get(self, muscle_group):
        """
        Get exercises for a specific muscle group
        
        This endpoint fetches all exercises that target the specified muscle group.
        Only authenticated users can access this endpoint.
        
        **Headers:**
        - Authorization: Bearer <access_token>
        
        **Parameters:**
        - muscle_group: The muscle group to filter by (e.g., 'chest', 'legs')
        
        **Returns:**
        - List of exercises for the specified muscle group
        - Count of exercises found
        """
        try:
            from services.exercise_service import ExerciseService
            response_data, status_code = ExerciseService.get_exercises_by_muscle_group(muscle_group)
            return response_data, status_code
        except Exception as e:
            return {'error': 'Internal server error'}, 500 