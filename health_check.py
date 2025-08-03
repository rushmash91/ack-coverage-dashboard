import http.server
import socketserver
import threading
import subprocess
import sys
import time

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/health', '/']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

def start_health_server():
    """Start a simple health check server on port 8502"""
    with socketserver.TCPServer(("", 8502), HealthHandler) as httpd:
        httpd.serve_forever()

def main():
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    print("Health check server started on port 8502")
    time.sleep(1) 
    
    cmd = [
        "uv", "run", "python", "-m", "streamlit", "run", "main.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.fileWatcherType=none"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()