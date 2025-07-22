from typing import Dict, List, Tuple
from flask import current_app
from models.exercise import Exercise, db

class ExerciseService:
    """Service class for exercise operations."""
    
    @staticmethod
    def get_exercises_grouped_by_primary_muscles() -> Tuple[Dict, int]:
        """
        Fetch all exercises and group them by primary muscles.
        
        Groups exercises by the first muscle in the primary_muscles array.
        Returns a dictionary where keys are muscle groups and values are lists of exercises.
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Fetch all exercises from the database
            exercises = Exercise.query.all()
            
            if not exercises:
                return {
                    'message': 'No exercises found',
                    'exercises': {}
                }, 200
            
            # Group exercises by primary muscle (first muscle in primary_muscles array)
            grouped_exercises = {}
            
            for exercise in exercises:
                # Get the first muscle from primary_muscles array as the grouping key
                if exercise.primary_muscles and len(exercise.primary_muscles) > 0:
                    primary_muscle = exercise.primary_muscles[0].lower()
                    
                    # Initialize the muscle group if it doesn't exist
                    if primary_muscle not in grouped_exercises:
                        grouped_exercises[primary_muscle] = []
                    
                    # Add the exercise to the appropriate muscle group
                    grouped_exercises[primary_muscle].append(exercise.to_dict())
                else:
                    # Handle exercises without primary muscles
                    if 'other' not in grouped_exercises:
                        grouped_exercises['other'] = []
                    grouped_exercises['other'].append(exercise.to_dict())
            
            # Sort muscle groups alphabetically
            sorted_grouped_exercises = dict(sorted(grouped_exercises.items()))
            
            return {
                'message': 'Exercises retrieved successfully',
                'exercises': sorted_grouped_exercises,
                'total_muscle_groups': len(sorted_grouped_exercises),
                'total_exercises': len(exercises)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching exercises: {str(e)}")
            return {
                'error': 'Internal server error',
                'message': 'Failed to fetch exercises'
            }, 500
    
    @staticmethod
    def get_exercises_by_muscle_group(muscle_group: str) -> Tuple[Dict, int]:
        """
        Fetch exercises for a specific muscle group.
        
        Args:
            muscle_group: The muscle group to filter by
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Fetch exercises where the first primary muscle matches the requested group
            exercises = Exercise.query.filter(
                Exercise.primary_muscles.any(muscle_group.lower())
            ).all()
            
            if not exercises:
                return {
                    'message': f'No exercises found for muscle group: {muscle_group}',
                    'exercises': []
                }, 200
            
            exercise_list = [exercise.to_dict() for exercise in exercises]
            
            return {
                'message': f'Exercises for {muscle_group} retrieved successfully',
                'muscle_group': muscle_group,
                'exercises': exercise_list,
                'count': len(exercise_list)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching exercises for muscle group {muscle_group}: {str(e)}")
            return {
                'error': 'Internal server error',
                'message': 'Failed to fetch exercises for muscle group'
            }, 500
    
    @staticmethod
    def get_available_muscle_groups() -> Tuple[Dict, int]:
        """
        Get list of all available muscle groups.
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Get all unique primary muscles from the database
            exercises = Exercise.query.all()
            
            muscle_groups = set()
            
            for exercise in exercises:
                if exercise.primary_muscles:
                    for muscle in exercise.primary_muscles:
                        muscle_groups.add(muscle.lower())
            
            sorted_muscle_groups = sorted(list(muscle_groups))
            
            return {
                'message': 'Muscle groups retrieved successfully',
                'muscle_groups': sorted_muscle_groups,
                'count': len(sorted_muscle_groups)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching muscle groups: {str(e)}")
            return {
                'error': 'Internal server error',
                'message': 'Failed to fetch muscle groups'
            }, 500 