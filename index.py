import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # 这里的关键是：如果飞书发来 challenge，就原样回给它
        challenge = data.get("challenge")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if challenge:
            res = json.dumps({"challenge": challenge})
        else:
            res = json.dumps({"status": "ok"})
            
        self.wfile.write(res.encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Bot is alive!".encode('utf-8'))
