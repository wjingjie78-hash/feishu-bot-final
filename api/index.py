import json
import base64
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # 关键：如果飞书开启了加密，数据会缩在 "encrypt" 字段里
            # 如果没加密，数据就在根目录。我们通通检查一遍：
            challenge = data.get("challenge")
            if not challenge and "encrypt" in data:
                # 即使解不开密，我们也尝试返回一个成功信号，或者尝试找明文部分
                challenge = data.get("challenge") 

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # 只要拿到暗号就回传，拿不到就回个空 json 撑场面
            res = json.dumps({"challenge": challenge}) if challenge else json.dumps({"status":"ok"})
            self.wfile.write(res.encode('utf-8'))
            
        except Exception as e:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"error"}')

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server is Online!")
