import os
import sys
from app import TrainingReportHandler
import http.server
import socketserver

# WSGI application object for gunicorn
def create_app():
    return TrainingReportHandler

# For direct execution
if __name__ == '__main__':
    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))
    
    # Create the server
    with socketserver.TCPServer(("0.0.0.0", port), TrainingReportHandler) as httpd:
        print(f"🚀 Starting Stellantis Training Report Processor...")
        print(f"📡 Port: {port}")
        print(f"🌐 Host: 0.0.0.0")
        print(f"🔗 Health check at: /health")
        print(f"📊 Full training report functionality ready!")
        print(f"✅ Server started on port {port}")
        httpd.serve_forever()

# WSGI application for gunicorn
app = create_app()
