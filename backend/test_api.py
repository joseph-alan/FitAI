#!/usr/bin/env python3
"""
Test script for the Workout API.
This script tests the registration and login endpoints.
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            return True
        else:
            print(f"❌ Health check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        return False

def test_user_registration():
    """Test user registration endpoint."""
    print("\n🔍 Testing user registration...")
    
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "date_of_birth": "1990-01-01",
        "gender": "male"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ User registration successful!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Access Token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Registration failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return None

def test_user_login():
    """Test user login endpoint."""
    print("\n🔍 Testing user login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User login successful!")
            print(f"   Access Token: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def test_get_profile(access_token):
    """Test getting user profile with JWT token."""
    print("\n🔍 Testing get profile endpoint...")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/auth/profile",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Get profile successful!")
            print(f"   User: {data['user']['first_name']} {data['user']['last_name']}")
            print(f"   Email: {data['user']['email']}")
            return True
        else:
            print(f"❌ Get profile failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Get profile error: {str(e)}")
        return False

def main():
    """Main function to run all tests."""
    print("🚀 Starting Workout API tests...\n")
    
    # Test health check
    if not test_health_check():
        print("\n❌ Health check failed. Stopping tests.")
        sys.exit(1)
    
    # Test registration
    access_token = test_user_registration()
    if not access_token:
        print("\n❌ Registration failed. Stopping tests.")
        sys.exit(1)
    
    # Test login
    login_token = test_user_login()
    if not login_token:
        print("\n❌ Login failed. Stopping tests.")
        sys.exit(1)
    
    # Test get profile
    if not test_get_profile(access_token):
        print("\n❌ Get profile failed.")
        sys.exit(1)
    
    print("\n🎉 All tests passed successfully!")
    print("The Workout API is working correctly.")

if __name__ == "__main__":
    main() 