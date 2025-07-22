#!/usr/bin/env python3
"""
Run script for the Workout API.
This script starts the Flask application with proper configuration.
"""

import os
from dotenv import load_dotenv
from app import create_app

def main():
    """Main function to run the Flask application."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Create Flask app
    app = create_app()
    
    # Get configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Workout API on {host}:{port}")
    print(f"📊 Debug mode: {'enabled' if debug else 'disabled'}")
    print(f"🔗 Health check: http://{host}:{port}/health")
    print(f"📚 API docs: Check README.md for endpoint documentation")
    print("Press Ctrl+C to stop the server\n")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main() 