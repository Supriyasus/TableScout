"""
WSGI entry point for production deployment on Render/Heroku
"""
import os
from backend.main import app

# This file allows gunicorn to properly load the FastAPI app
if __name__ == "__main__":
    app.run()
