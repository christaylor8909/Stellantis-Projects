# Import the Flask app from flask_app.py
from flask_app import app

# This allows gunicorn to find the app with the command: gunicorn app:app
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
