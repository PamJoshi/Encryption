#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
from http import HTTPStatus
import tempfile
import os

class EncryptionHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/':
            response = {
                "message": "Welcome to the Simple Encryption Service API!",
                "status": "running",
                "note": "This is a simplified version for testing"
            }
        elif self.path == '/health' or self.path == '/api/health':
            response = {"status": "healthy", "message": "Simple encryption service is running"}
        elif self.path.startswith('/generate-key') or self.path.startswith('/api/generate-key'):
            # Simple key generation
            import secrets
            import base64
            key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
            response = {"key": key, "algorithm": "aes256"}
        else:
            response = {"error": "Endpoint not found"}
            
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests"""
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/encrypt' or self.path == '/api/encrypt':
            try:
                # Read the content length
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # For now, just return a success response
                response = {
                    "original_file": "test_file.txt",
                    "encrypted_file": "/download/temp123/test_file.txt.enc",
                    "algorithm": "aes256",
                    "message": "File encrypted successfully (mock response)"
                }
                
            except Exception as e:
                response = {"error": f"Encryption failed: {str(e)}"}
        else:
            response = {"error": "Endpoint not found"}
            
        self.wfile.write(json.dumps(response).encode())

def run_server(port=8000):
    """Run the simple server"""
    with socketserver.TCPServer(("", port), EncryptionHandler) as httpd:
        print(f"Simple encryption server running on http://localhost:{port}")
        print("This is a mock server for testing the frontend connection")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    run_server()