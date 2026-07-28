#!/usr/bin/env python3
"""HTTPS server with frontend-JS password protection."""
import http.server
import os
import ssl
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3211
WEB_ROOT = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(WEB_ROOT, 'ssl', 'cert.pem')
KEY  = os.path.join(WEB_ROOT, 'ssl', 'key.pem')

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        rel = os.path.relpath(path, os.getcwd())
        if rel.startswith('..'):
            return os.path.join(WEB_ROOT, rel)
        return path

if __name__ == '__main__':
    os.chdir(WEB_ROOT)
    server = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    server.socket = ssl.wrap_socket(server.socket,
                                    certfile=CERT,
                                    keyfile=KEY,
                                    server_side=True)
    print(f"HTTPS serving on https://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
