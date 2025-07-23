# Workout Backend API

A Flask-based REST API for workout management with user authentication using JWT tokens.

## 📚 **Documentation**

📖 **Complete documentation is available in the [`docs/`](docs/) folder:**

- [📋 API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [🚀 Production Deployment](docs/PRODUCTION_DEPLOYMENT.md) - Deployment guide
- [🗄️ Database Setup](docs/DATABASE_SETUP_GUIDE.md) - Database configuration
- [🔐 JWT Authentication](docs/JWT_USER_IDENTIFICATION.md) - Authentication guide
- [🐛 Error Handling](docs/ERROR_HANDLING_FIX.md) - Troubleshooting guide

## Features

- User registration and authentication
- JWT token-based authentication
- PostgreSQL database integration
- Input validation using Marshmallow
- Password hashing with bcrypt
- RESTful API design
- Exercise management with muscle group grouping
- Swagger API documentation

## Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost/workout
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   ```

5. **Set up the database**
   ```bash
   # Initialize migrations
   flask db init
   
   # Create initial migration
   flask db migrate -m "Initial migration"
   
   # Apply migrations
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

#### Register User
- **URL**: `POST /api/auth/register`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "gender": "male",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "is_active": true
    },
    "access_token": "jwt_token",
    "refresh_token": "refresh_token"
  }
  ```

#### Login User
- **URL**: `POST /api/auth/login`
- **Description**: Authenticate user and get JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "gender": "male",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "is_active": true
    },
    "access_token": "jwt_token",
    "refresh_token": "refresh_token"
  }
  ```

#### Get User Profile
- **URL**: `GET /api/auth/profile`
- **Description**: Get current user profile
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "message": "Profile retrieved successfully",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "gender": "male",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "is_active": true
    }
  }
  ```

#### Refresh Token
- **URL**: `POST /api/auth/refresh`
- **Description**: Refresh access token using refresh token
- **Headers**: `Authorization: Bearer <refresh_token>`
- **Response**:
  ```json
  {
    "message": "Token refreshed successfully",
    "access_token": "new_jwt_token"
  }
  ```

### Health Check
- **URL**: `GET /health`
- **Description**: Check API health status
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "Workout API is running"
  }
  ```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials or missing token
- `404 Not Found`: Resource not found
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server error

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Input validation and sanitization
- CORS support for cross-origin requests
- Environment variable configuration

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migrations
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## Production Deployment

1. Set appropriate environment variables
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure proper logging
4. Set up monitoring and health checks
5. Use HTTPS in production
6. Regularly update dependencies

## License

This project is licensed under the MIT License. 