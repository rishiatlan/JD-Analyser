from app.main import app
import os

# This is the WSGI application that gunicorn will use
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port) 