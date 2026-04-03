import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}

        # 飞书核心验证：获取 challenge
        challenge = data.get("challenge")
        
        # 必须严格返回 200 状态码
        self.send_response(200)
        # 必须严格声明返回的是 JSON 格式
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if challenge:
            # 飞书要求返回必须是 {"challenge": "原来的暗号"}
            res = json.dumps({"challenge": challenge})
            self.wfile.write(res.encode('utf-8'))
        else:
            # 这里的 success 也是为了让飞书闭嘴
            res = json.dumps({"status": "success"})
            self.wfile.write(res.encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Vercel is Alive!".encode('utf-8'))
