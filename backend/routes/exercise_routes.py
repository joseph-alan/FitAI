from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.exercise_service import ExerciseService

exercise_bp = Blueprint('exercise', __name__, url_prefix='/api/exercises')

@exercise_bp.route('/grouped', methods=['GET'])
@jwt_required()
def get_exercises_grouped():
    """
    Get all exercises grouped by primary muscles.
    
    This endpoint fetches all exercises from the database and groups them
    by the first muscle in the primary_muscles array. Only authenticated users
    can access this endpoint.
    
    **Headers:**
    - Authorization: Bearer <access_token>
    
    **Returns:**
    - Dictionary with muscle groups as keys and lists of exercises as values
    """
    try:
        response_data, status_code = ExerciseService.get_exercises_grouped_by_primary_muscles()
        return jsonify(response_data), status_code
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@exercise_bp.route('/muscle-groups', methods=['GET'])
@jwt_required()
def get_muscle_groups():
    """
    Get all available muscle groups.
    
    This endpoint returns a list of all unique muscle groups available
    in the exercises database. Only authenticated users can access this endpoint.
    
    **Headers:**
    - Authorization: Bearer <access_token>
    
    **Returns:**
    - List of available muscle groups
    """
    try:
        response_data, status_code = ExerciseService.get_available_muscle_groups()
        return jsonify(response_data), status_code
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@exercise_bp.route('/muscle-group/<muscle_group>', methods=['GET'])
@jwt_required()
def get_exercises_by_muscle_group(muscle_group):
    """
    Get exercises for a specific muscle group.
    
    This endpoint fetches all exercises that target the specified muscle group.
    Only authenticated users can access this endpoint.
    
    **Headers:**
    - Authorization: Bearer <access_token>
    
    **Parameters:**
    - muscle_group: The muscle group to filter by (e.g., 'chest', 'legs')
    
    **Returns:**
    - List of exercises for the specified muscle group
    """
    try:
        response_data, status_code = ExerciseService.get_exercises_by_muscle_group(muscle_group)
        return jsonify(response_data), status_code
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 