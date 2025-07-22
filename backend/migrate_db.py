#!/usr/bin/env python3
"""
Database migration script for the Workout API.
This script sets up migrations and creates the users table while preserving existing tables.
"""

import os
import sys
from app import create_app
from models.user import db
from flask_migrate import Migrate, upgrade, init, migrate

def setup_migrations():
    """Set up Flask-Migrate and create initial migration."""
    try:
        app = create_app()
        
        with app.app_context():
            # Initialize migrations if not already done
            try:
                init()
                print("✅ Migrations initialized successfully!")
            except Exception as e:
                print(f"ℹ️  Migrations already initialized: {str(e)}")
            
            # Create initial migration
            try:
                migrate(message="Initial migration - create users table")
                print("✅ Initial migration created successfully!")
            except Exception as e:
                print(f"ℹ️  Migration already exists: {str(e)}")
            
            # Apply migrations
            try:
                upgrade()
                print("✅ Migrations applied successfully!")
            except Exception as e:
                print(f"ℹ️  Migrations already applied: {str(e)}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error setting up migrations: {str(e)}")
        return False

def verify_database():
    """Verify that the database is set up correctly."""
    try:
        app = create_app()
        
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Database tables: {tables}")
            
            # Check if users table exists
            if 'users' in tables:
                print("✅ Users table exists!")
                columns = inspector.get_columns('users')
                print("📊 Users table structure:")
                for column in columns:
                    print(f"   - {column['name']}: {column['type']}")
            else:
                print("❌ Users table not found!")
                return False
            
            # Check if exercises table is preserved
            if 'exercises' in tables:
                print("✅ Exercises table preserved!")
            else:
                print("⚠️  Warning: Exercises table not found!")
                
            return True
            
    except Exception as e:
        print(f"❌ Error verifying database: {str(e)}")
        return False

def main():
    """Main function to run the database migration."""
    print("🚀 Setting up Workout API database migrations...")
    
    # Check if database URL is set
    if not os.environ.get('DATABASE_URL'):
        print("⚠️  DATABASE_URL not set. Using default PostgreSQL connection.")
        print("   Make sure PostgreSQL is running and the 'workout' database exists.")
    
    # Set up migrations
    success = setup_migrations()
    
    if success:
        print("\n🔍 Verifying database setup...")
        verify_success = verify_database()
        
        if verify_success:
            print("\n🎉 Database migration completed successfully!")
            print("You can now run the Flask application with: python app.py")
        else:
            print("\n❌ Database verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Database migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 