import os
import http.server
import socketserver

# Simple HTTP server for Railway
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("STELLANTIS Training Report Processor - Ready! 🚀".encode('utf-8'))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = f'{{"status": "healthy", "message": "STELLANTIS Training Report Processor is running", "port": "{os.environ.get("PORT", "5000")}"}}'
            self.wfile.write(response.encode())
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("App is working! ✅".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting simple HTTP server...")
    print(f"📡 Port: {port}")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔗 Health check at: /health")
    
    with socketserver.TCPServer(("0.0.0.0", port), SimpleHandler) as httpd:
        print(f"✅ Server started on port {port}")
        httpd.serve_forever()
