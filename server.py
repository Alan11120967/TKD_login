# TK.d 登录页本地服务器
# 用法: python server.py
# 访问: http://127.0.0.1:8000

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, threading, webbrowser

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 关闭日志输出

    def do_GET(self):
        # 访问根路径 / 时，直接返回 index.html
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        
        # 确保路径不会跳出当前目录（安全限制）
        filepath = self.path.lstrip("/")
        base = os.path.abspath(".")
        full = os.path.abspath(os.path.join(base, filepath))
        if not full.startswith(base):
            self.send_error(403, "Forbidden")
            return
        
        return SimpleHTTPRequestHandler.do_GET(self)

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("TK.d 登录页已启动")
print("访问地址: http://127.0.0.1:8000")
print("按 Ctrl+C 停止服务")

# 1秒后自动打开浏览器
threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:8000")).start()

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n服务已停止")
    server.server_close()