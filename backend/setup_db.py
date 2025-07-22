#!/usr/bin/env python3
"""
Database setup script for the Workout API.
This script initializes the database and creates the users table.
"""

import os
import sys
from app import create_app
from models.user import db

def setup_database():
    """Set up the database and create tables."""
    try:
        app = create_app()
        
        with app.app_context():
            # Check existing tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"📋 Existing tables: {existing_tables}")
            
            # Create only the users table (don't touch exercises table)
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify the users table exists
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'users' in tables:
                print("✅ Users table created successfully!")
                
                # Show table structure
                if 'users' in tables:
                    columns = inspector.get_columns('users')
                    print("📊 Users table structure:")
                    for column in columns:
                        print(f"   - {column['name']}: {column['type']}")
                        
            else:
                print("❌ Users table not found!")
                return False
            
            # Verify exercises table is preserved
            if 'exercises' in tables:
                print("✅ Exercises table preserved successfully!")
            else:
                print("⚠️  Warning: Exercises table not found!")
                
            return True
            
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def main():
    """Main function to run the database setup."""
    print("🚀 Setting up Workout API database...")
    
    # Check if database URL is set
    if not os.environ.get('DATABASE_URL'):
        print("⚠️  DATABASE_URL not set. Using default PostgreSQL connection.")
        print("   Make sure PostgreSQL is running and the 'workout' database exists.")
    
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the Flask application with: python app.py")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 