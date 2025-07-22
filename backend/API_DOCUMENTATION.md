# Workout API Documentation

## 🌐 API Base URL
```
http://localhost:5000
```

## 📚 Swagger Documentation
**Interactive API Documentation**: http://localhost:5000/docs

## 🔐 Authentication
The API uses JWT (JSON Web Token) authentication. Most endpoints require a valid JWT token in the Authorization header.

**Header Format:**
```
Authorization: Bearer <your_jwt_token>
```

## 📋 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Workout API is running"
}
```

---

### 2. User Registration
**POST** `/api/auth/register`

Register a new user account.

**Request Body:**
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

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "is_active": true
  },
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input data
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server error

---

### 3. User Login
**POST** `/api/auth/login`

Authenticate user and get JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "is_active": true
  },
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Server error

---

### 4. Get User Profile
**GET** `/api/auth/profile`

Get current user's profile information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Profile retrieved successfully",
  "user": {
    "id": "uuid-string",
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

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error

---

### 5. Refresh Token
**POST** `/api/auth/refresh`

Get a new access token using refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200 OK):**
```json
{
  "message": "Token refreshed successfully",
  "access_token": "new_jwt_access_token"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid refresh token
- `500 Internal Server Error`: Server error

---

## 🔧 Usage Examples

### Using cURL

#### 1. Register a new user:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "male"
  }'
```

#### 2. Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

#### 3. Get profile (with token):
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Refresh token:
```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

### Using JavaScript (Fetch API)

#### 1. Register a new user:
```javascript
const response = await fetch('http://localhost:5000/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'password123',
    first_name: 'John',
    last_name: 'Doe',
    date_of_birth: '1990-01-01',
    gender: 'male'
  })
});

const data = await response.json();
console.log(data);
```

#### 2. Login:
```javascript
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'password123'
  })
});

const data = await response.json();
const accessToken = data.access_token;
```

#### 3. Get profile:
```javascript
const response = await fetch('http://localhost:5000/api/auth/profile', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  }
});

const data = await response.json();
console.log(data);
```

---

## 🔒 Security Features

### JWT Token Management
- **Access Token**: Valid for 1 hour
- **Refresh Token**: Valid for 30 days
- **Automatic Token Refresh**: Use refresh endpoint to get new access tokens

### Password Security
- **Bcrypt Hashing**: All passwords are securely hashed
- **Minimum Length**: Passwords must be at least 6 characters
- **No Plain Text Storage**: Passwords are never stored in plain text

### Input Validation
- **Email Validation**: Proper email format required
- **Date Validation**: Date of birth cannot be in the future
- **Gender Validation**: Must be 'male', 'female', or 'other'
- **Required Fields**: All registration fields are mandatory

---

## 📊 Response Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing authentication |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error - Server error |

---

## 🚀 Getting Started

### 1. Start the API Server
```bash
python3 run.py
```

### 2. Access Swagger Documentation
Open your browser and go to: http://localhost:5000/docs

### 3. Test the API
```bash
# Health check
curl http://localhost:5000/health

# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User","date_of_birth":"1990-01-01","gender":"male"}'
```

---

## 🔧 Development

### Environment Variables
Create a `.env` file with the following variables:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost/workout
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
```

### Database Setup
```bash
python3 setup_db.py
```

### Running Tests
```bash
python3 test_api.py
```

---

## 📝 Notes

- The API uses PostgreSQL as the database
- JWT tokens are used for authentication
- All passwords are hashed using bcrypt
- CORS is enabled for cross-origin requests
- The API includes comprehensive error handling
- Swagger documentation is available at `/docs`

---

**API Version**: 1.0  
**Last Updated**: 2024  
**Base URL**: http://localhost:5000 