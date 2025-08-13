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

# Minimal startup for Railway
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting minimal STELLANTIS app...")
    print(f"📡 Port: {port}")
    print(f"🌐 Host: 0.0.0.0")
    
    try:
        app.run(
            debug=False,
            host='0.0.0.0',
            port=port,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
