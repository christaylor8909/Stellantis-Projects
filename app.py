from flask import Flask, jsonify
import os

# Create minimal Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return "STELLANTIS Training Report Processor - Ready! 🚀"

@app.route('/health')
def health_check():
    """Simple health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy', 
        'message': 'STELLANTIS Training Report Processor is running',
        'port': os.environ.get('PORT', '5000')
    })

@app.route('/test')
def test():
    """Simple test endpoint"""
    return "App is working! ✅"

# App is ready for gunicorn
print(f"🚀 STELLANTIS app loaded and ready!")
print(f"📡 Will bind to port: {os.environ.get('PORT', '5000')}")
print(f"🌐 Health check at: /")
print(f"🔗 Test endpoint at: /test")
