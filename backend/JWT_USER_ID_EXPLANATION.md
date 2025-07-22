# JWT User ID Explanation

## 🎯 **The `sub` Field IS the User ID**

### **📋 Your JWT Token Analysis:**

You correctly decoded your JWT token and found:
```json
{
  "fresh": false,
  "iat": 1753160636,
  "jti": "a93ba1f1-13d4-41cd-aaa4-21776c24f0dd",
  "type": "access",
  "sub": "80320293-4508-448e-974d-ee9abc9f42ec",  // ← THIS IS THE USER ID
  "nbf": 1753160636,
  "exp": 1753164236
}
```

### **🔍 JWT Standard Claims:**

- **`sub`** = **Subject** (the user ID in our case)
- **`iat`** = Issued At timestamp
- **`exp`** = Expires At timestamp
- **`jti`** = JWT ID (unique token identifier)
- **`type`** = Token type (access/refresh)
- **`nbf`** = Not Before timestamp

### **🔧 How It Works in Our Code:**

#### **1. Token Creation (Login/Register):**
```python
# In AuthService.login_user() and register_user()
user = User.query.filter_by(email=validated_data['email']).first()
access_token = create_access_token(identity=str(user.id))
```

**What happens:**
- `user.id` = `"80320293-4508-448e-974d-ee9abc9f42ec"`
- `identity=str(user.id)` → This becomes the `sub` claim
- JWT token contains: `"sub": "80320293-4508-448e-974d-ee9abc9f42ec"`

#### **2. Token Decoding (Protected Routes):**
```python
# In routes/auth_routes.py
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()  # Gets the 'sub' value
    user = AuthService.get_user_by_id(current_user_id)
```

**What happens:**
- `get_jwt_identity()` extracts the `sub` claim
- Returns: `"80320293-4508-448e-974d-ee9abc9f42ec"`
- This is used to query the database for the user

### **🎯 JWT Standard vs Our Implementation:**

#### **JWT Standard:**
- **`sub`** = Subject (can be any identifier)
- **`iss`** = Issuer
- **`aud`** = Audience
- **`exp`** = Expiration
- **`iat`** = Issued At

#### **Our Implementation:**
- **`sub`** = User ID (UUID string)
- **`type`** = Token type (access/refresh)
- **`exp`** = Expiration (1 hour for access)
- **`iat`** = Issued At
- **`jti`** = Unique token ID

### **🔍 Verification Process:**

#### **1. Token Creation:**
```
User logs in → User ID: "80320293-4508-448e-974d-ee9abc9f42ec"
→ create_access_token(identity=user_id)
→ JWT contains: "sub": "80320293-4508-448e-974d-ee9abc9f42ec"
```

#### **2. Token Usage:**
```
Client sends JWT → Server decodes
→ get_jwt_identity() returns: "80320293-4508-448e-974d-ee9abc9f42ec"
→ User.query.get("80320293-4508-448e-974d-ee9abc9f42ec")
→ Returns user object
```

### **📊 User Identification Flow:**

```
1. User logs in with email/password
2. Server validates credentials
3. Server creates JWT with user ID as 'sub' claim
4. Client stores JWT token
5. Client sends JWT in Authorization header
6. Server decodes JWT and extracts 'sub' (user ID)
7. Server queries database with user ID
8. Server returns user-specific data
```

### **🎯 Why `sub` Instead of `user_id`:**

#### **JWT Standards:**
- JWT follows RFC 7519 standard
- `sub` is the standard claim for subject/principal
- Using standard claims ensures compatibility
- Other systems expect `sub` for subject identification

#### **Our Implementation:**
```python
# We could have used a custom claim like:
create_access_token(identity=user.id, user_id=user.id)

# But we use the standard approach:
create_access_token(identity=user.id)  # identity becomes 'sub'
```

### **🔧 Code Examples:**

#### **Creating Token:**
```python
# User object
user = User.query.filter_by(email="user@example.com").first()
# user.id = "80320293-4508-448e-974d-ee9abc9f42ec"

# Create token
token = create_access_token(identity=str(user.id))
# Result: JWT with "sub": "80320293-4508-448e-974d-ee9abc9f42ec"
```

#### **Using Token:**
```python
@jwt_required()
def protected_endpoint():
    user_id = get_jwt_identity()  # Gets "80320293-4508-448e-974d-ee9abc9f42ec"
    user = User.query.get(user_id)  # Finds user by ID
    return jsonify({"user": user.to_dict()})
```

### **📝 Summary:**

**You're absolutely correct!** The `sub` field in your JWT token **IS** the user ID. 

- ✅ **`sub`** = User ID (UUID string)
- ✅ **`get_jwt_identity()`** extracts the `sub` value
- ✅ **User identification** works through the `sub` claim
- ✅ **Standard JWT practice** uses `sub` for subject identification

The JWT token contains your user ID in the `sub` claim, and our code extracts it using `get_jwt_identity()` to identify which user is making the request. 