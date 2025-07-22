from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class UserRegistrationSchema(Schema):
    """Schema for user registration validation."""
    
    email = fields.Email(required=True, validate=validate.Length(min=5, max=120))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    
    def validate_date_of_birth(self, value):
        """Validate that date of birth is not in the future."""
        if value > datetime.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
        return value

class UserLoginSchema(Schema):
    """Schema for user login validation."""
    
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserResponseSchema(Schema):
    """Schema for user response data."""
    
    id = fields.Str()
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    date_of_birth = fields.Date()
    gender = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_active = fields.Bool() 