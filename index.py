import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. 读取飞书发来的数据
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # 2. 解析数据
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}

        # 3. 核心：如果飞书在验证地址，它会发来一个 challenge，我们必须原样吐回去
        challenge = data.get("challenge")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if challenge:
            # 返回飞书要求的格式
            res = json.dumps({"challenge": challenge})
        else:
            # 正常运行状态
            res = json.dumps({"status": "ready"})
            
        self.wfile.write(res.encode('utf-8'))

    def do_GET(self):
        # 浏览器访问时显示这个
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Bot is Ready and Waiting!".encode('utf-8'))
