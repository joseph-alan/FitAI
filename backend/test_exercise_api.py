#!/usr/bin/env python3
"""
Test script for the Exercise API endpoints.
This script tests the exercise endpoints with authentication.
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:5000"

def get_access_token():
    """Get access token by logging in."""
    print("🔑 Getting access token...")
    
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
            print("✅ Login successful!")
            return data['access_token']
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def test_exercises_grouped(access_token):
    """Test getting exercises grouped by primary muscles."""
    print("\n🔍 Testing exercises grouped by primary muscles...")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/exercises/grouped",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Exercises grouped successfully!")
            print(f"   Total muscle groups: {data['total_muscle_groups']}")
            print(f"   Total exercises: {data['total_exercises']}")
            
            # Show first few muscle groups
            muscle_groups = list(data['exercises'].keys())[:5]
            print(f"   Sample muscle groups: {muscle_groups}")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_muscle_groups(access_token):
    """Test getting available muscle groups."""
    print("\n🔍 Testing muscle groups endpoint...")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/exercises/muscle-groups",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Muscle groups retrieved successfully!")
            print(f"   Total muscle groups: {data['count']}")
            print(f"   Sample groups: {data['muscle_groups'][:5]}")
            return data['muscle_groups']
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_exercises_by_muscle_group(access_token, muscle_group):
    """Test getting exercises for a specific muscle group."""
    print(f"\n🔍 Testing exercises for muscle group: {muscle_group}...")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/exercises/muscle-group/{muscle_group}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Exercises for {muscle_group} retrieved successfully!")
            print(f"   Exercise count: {data['count']}")
            if data['exercises']:
                print(f"   Sample exercise: {data['exercises'][0]['name']}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_unauthorized_access():
    """Test that unauthorized access is properly blocked."""
    print("\n🔍 Testing unauthorized access...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/exercises/grouped")
        
        if response.status_code == 401:
            print("✅ Unauthorized access properly blocked!")
            return True
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function to run all exercise API tests."""
    print("🚀 Starting Exercise API tests...\n")
    
    # Get access token
    access_token = get_access_token()
    if not access_token:
        print("\n❌ Failed to get access token. Stopping tests.")
        sys.exit(1)
    
    # Test exercises grouped
    if not test_exercises_grouped(access_token):
        print("\n❌ Exercises grouped test failed.")
        sys.exit(1)
    
    # Test muscle groups
    muscle_groups = test_muscle_groups(access_token)
    if not muscle_groups:
        print("\n❌ Muscle groups test failed.")
        sys.exit(1)
    
    # Test exercises by muscle group (test with first available group)
    if muscle_groups:
        test_muscle = muscle_groups[0]
        if not test_exercises_by_muscle_group(access_token, test_muscle):
            print(f"\n❌ Exercises by muscle group test failed for {test_muscle}.")
            sys.exit(1)
    
    # Test unauthorized access
    if not test_unauthorized_access():
        print("\n❌ Unauthorized access test failed.")
        sys.exit(1)
    
    print("\n🎉 All Exercise API tests passed successfully!")
    print("The Exercise API is working correctly with proper authentication.")

if __name__ == "__main__":
    main() 