import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# This is the WSGI application that gunicorn will use
application = app 