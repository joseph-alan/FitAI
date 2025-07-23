# Workout API Documentation

## 📚 **Documentation Index**

Welcome to the Workout API documentation! This folder contains comprehensive guides for setting up, deploying, and understanding the Workout API.

### **🚀 Getting Started**

#### **1. [API Documentation](API_DOCUMENTATION.md)**
- Complete API endpoint reference
- Request/response examples
- Authentication requirements
- Error handling guide

#### **2. [Database Setup Guide](DATABASE_SETUP_GUIDE.md)**
- How to set up the database
- Working with existing exercises table
- Automatic table creation
- Troubleshooting database issues

#### **3. [Production Deployment](PRODUCTION_DEPLOYMENT.md)**
- Environment variables for production
- Security best practices
- Deployment examples (Docker, Heroku, AWS, etc.)
- Production checklist

### **🔐 Authentication & Security**

#### **4. [JWT User Identification](JWT_USER_IDENTIFICATION.md)**
- How JWT tokens identify users
- Token structure and claims
- User context in protected routes
- Security features

#### **5. [JWT User ID Explanation](JWT_USER_ID_EXPLANATION.md)**
- Understanding the `sub` field in JWT tokens
- JWT standard claims
- How user identification works
- Code examples

### **🐛 Error Handling & Debugging**

#### **6. [Error Handling Fix](ERROR_HANDLING_FIX.md)**
- How 500 errors were resolved
- Enhanced error handling
- Better error messages
- Testing error scenarios

### **📊 API Features**

#### **7. [Exercise API Summary](EXERCISE_API_SUMMARY.md)**
- Exercise endpoints overview
- Grouped exercises by muscle groups
- Authentication requirements
- API testing guide

### **🛠️ Development & Migration**

#### **8. [Migration Summary](MIGRATION_SUMMARY.md)**
- Database migration process
- Preserving existing tables
- Migration verification
- Setup instructions

#### **9. [Swagger Summary](SWAGGER_SUMMARY.md)**
- API documentation setup
- Swagger UI integration
- Interactive API testing
- Documentation standards

---

## 📋 **Quick Reference**

### **Essential Commands:**
```bash
# Start the application
python3 run.py

# Set up database
python3 setup_db.py

# Run migrations
python3 migrate_db.py

# Test API
python3 test_api.py

# Test Exercise API
python3 test_exercise_api.py
```

### **Key Environment Variables:**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/workout
```

### **API Endpoints:**
- **Authentication**: `/api/auth/register`, `/api/auth/login`
- **User Profile**: `/api/auth/profile`
- **Exercises**: `/api/exercises/grouped`, `/api/exercises/muscle-groups`
- **Health Check**: `/health`
- **API Docs**: `/docs`

---

## 🎯 **Documentation Categories**

### **📖 Setup & Installation**
- [Database Setup Guide](DATABASE_SETUP_GUIDE.md)
- [Production Deployment](PRODUCTION_DEPLOYMENT.md)
- [Migration Summary](MIGRATION_SUMMARY.md)

### **🔐 Authentication & Security**
- [JWT User Identification](JWT_USER_IDENTIFICATION.md)
- [JWT User ID Explanation](JWT_USER_ID_EXPLANATION.md)
- [Error Handling Fix](ERROR_HANDLING_FIX.md)

### **📊 API Reference**
- [API Documentation](API_DOCUMENTATION.md)
- [Exercise API Summary](EXERCISE_API_SUMMARY.md)
- [Swagger Summary](SWAGGER_SUMMARY.md)

---

## 🚀 **Quick Start Guide**

### **1. Local Development:**
```bash
# Clone and setup
git clone <repository>
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
python3 setup_db.py

# Start application
python3 run.py
```

### **2. Production Deployment:**
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret-key
export DATABASE_URL=your-database-url

# Deploy
python3 run.py
```

### **3. Testing:**
```bash
# Test authentication
python3 test_api.py

# Test exercise endpoints
python3 test_exercise_api.py
```

---

## 📞 **Support**

If you need help with:
- **Setup issues**: Check [Database Setup Guide](DATABASE_SETUP_GUIDE.md)
- **Deployment problems**: See [Production Deployment](PRODUCTION_DEPLOYMENT.md)
- **API questions**: Review [API Documentation](API_DOCUMENTATION.md)
- **Authentication issues**: Read [JWT User Identification](JWT_USER_IDENTIFICATION.md)

---

## 📝 **Documentation Standards**

All documentation follows these standards:
- ✅ **Clear structure** with headers and sections
- ✅ **Code examples** for all features
- ✅ **Step-by-step guides** for complex processes
- ✅ **Troubleshooting sections** for common issues
- ✅ **Security best practices** highlighted
- ✅ **Production-ready** configurations

---

**🎉 Happy coding with the Workout API!** 