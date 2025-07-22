# JWT User Identification Guide

## 🎯 **Yes! JWT Tokens Identify Users**

### **📋 How It Works:**

#### **1. Token Creation (Login/Register):**
When a user logs in or registers, the JWT token is created with the user's ID as the `identity`:

```python
# In AuthService.login_user() and register_user()
access_token = create_access_token(identity=str(user.id))
refresh_token = create_refresh_token(identity=str(user.id))
```

#### **2. Token Content:**
The JWT token contains the user's ID in the `sub` (subject) claim:

```json
{
  "fresh": false,
  "iat": 1753160529,                    // Issued at
  "jti": "af648687-843b-450f-a611-e8337b8cc428",  // JWT ID
  "type": "access",                     // Token type
  "sub": "d434bf60-5fa8-4648-a155-8759fc562b3e",  // USER ID HERE!
  "nbf": 1753160529,                   // Not before
  "exp": 1753164129                    // Expires at
}
```

#### **3. Token Decoding (Protected Routes):**
When a protected route is accessed, the user ID is extracted from the token:

```python
# In routes/auth_routes.py - get_profile()
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()  # Gets the user ID from token
    user = AuthService.get_user_by_id(current_user_id)
```

### **🔍 Live Demonstration:**

#### **Step 1: Register a User**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "demo123",
    "first_name": "Demo",
    "last_name": "User",
    "date_of_birth": "1990-01-01",
    "gender": "male"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "message": "User registered successfully",
  "user": {
    "id": "d434bf60-5fa8-4648-a155-8759fc562b3e",
    "email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User"
  }
}
```

#### **Step 2: Use Token to Get User Profile**
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Response:**
```json
{
  "message": "Profile retrieved successfully",
  "user": {
    "id": "d434bf60-5fa8-4648-a155-8759fc562b3e",
    "email": "demo@example.com",
    "first_name": "Demo",
    "last_name": "User"
  }
}
```

### **🔐 How User Identification Works:**

#### **1. Token Structure:**
```
Header.Payload.Signature
```

**Header:**
```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

**Payload (Contains User ID):**
```json
{
  "sub": "d434bf60-5fa8-4648-a155-8759fc562b3e",  // ← USER ID
  "type": "access",
  "exp": 1753164129
}
```

#### **2. User Identification Flow:**
```
1. User logs in → JWT created with user ID
2. Client sends JWT in Authorization header
3. Server decodes JWT → extracts user ID
4. Server queries database → gets user data
5. Server returns user-specific response
```

### **🛡️ Security Features:**

#### **1. Token Expiration:**
- **Access Token**: 1 hour (configurable)
- **Refresh Token**: 30 days (configurable)

#### **2. Token Validation:**
- **Signature Verification**: Ensures token wasn't tampered with
- **Expiration Check**: Prevents use of expired tokens
- **Type Validation**: Distinguishes access vs refresh tokens

#### **3. User Context:**
```python
# In any protected route
@jwt_required()
def some_protected_endpoint():
    current_user_id = get_jwt_identity()  # Get user ID
    current_user = User.query.get(current_user_id)  # Get user object
    
    # Now you have full user context
    return jsonify({
        'message': f'Hello {current_user.first_name}!',
        'user_id': current_user_id
    })
```

### **📊 Available User Information:**

#### **From JWT Token:**
- ✅ **User ID** (`sub` claim)
- ✅ **Token Type** (access/refresh)
- ✅ **Issued At** (`iat`)
- ✅ **Expires At** (`exp`)

#### **From Database (via User ID):**
- ✅ **Email**
- ✅ **First Name**
- ✅ **Last Name**
- ✅ **Date of Birth**
- ✅ **Gender**
- ✅ **Account Status** (active/inactive)
- ✅ **Created/Updated Timestamps**

### **🎯 Usage Examples:**

#### **1. Get Current User Profile:**
```python
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(current_user_id)
    return jsonify({'user': user.to_dict()})
```

#### **2. User-Specific Data:**
```python
@jwt_required()
def get_user_exercises():
    current_user_id = get_jwt_identity()
    # Get exercises specific to this user
    user_exercises = ExerciseService.get_user_exercises(current_user_id)
    return jsonify({'exercises': user_exercises})
```

#### **3. User Permissions:**
```python
@jwt_required()
def admin_only_endpoint():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    return jsonify({'message': 'Admin access granted'})
```

### **🔧 Configuration:**

#### **JWT Settings (config.py):**
```python
JWT_SECRET_KEY = 'your-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
```

#### **Token Claims:**
- **`sub`**: User ID (primary identifier)
- **`type`**: Token type (access/refresh)
- **`exp`**: Expiration timestamp
- **`iat`**: Issued at timestamp
- **`jti`**: JWT ID (unique token identifier)

### **🚀 Benefits:**

1. **Stateless Authentication**: No server-side session storage
2. **User Context**: Always know which user is making the request
3. **Scalable**: Works across multiple servers
4. **Secure**: Cryptographically signed tokens
5. **Flexible**: Can include additional claims if needed

### **📝 Best Practices:**

#### **1. Always Validate User Context:**
```python
@jwt_required()
def user_specific_action():
    current_user_id = get_jwt_identity()
    # Always verify the user has permission for this action
    if not user_can_perform_action(current_user_id, action):
        return jsonify({'error': 'Permission denied'}), 403
```

#### **2. Handle Token Expiration:**
```python
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token has expired',
        'message': 'Please login again'
    }), 401
```

#### **3. Log User Actions:**
```python
@jwt_required()
def some_action():
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"User {current_user_id} performed action")
```

---

## 🎉 **Summary**

**Yes, you can absolutely identify which user is logged in from the JWT token!**

The JWT token contains the user's ID in the `sub` claim, and the `get_jwt_identity()` function extracts this ID, allowing you to:

- ✅ **Identify the user** making each request
- ✅ **Access user data** from the database
- ✅ **Enforce user-specific permissions**
- ✅ **Provide personalized responses**
- ✅ **Log user actions** for audit trails

The current setup provides a robust, secure way to identify users across all authenticated endpoints. 