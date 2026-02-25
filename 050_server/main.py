import http.server
import socketserver
import os
import signal
import sys
import json
import importlib.util
from datetime import datetime
from pathlib import Path

# 010_ai は数字始まりで通常importできないため
# importlib.util で直接ファイルパス指定
_core_path = os.path.join(
    os.path.dirname(__file__), "..", "010_ai", "core.py"
)
_spec = importlib.util.spec_from_file_location(
    "core", _core_path
)
_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_core)
Cabinet = _core.Cabinet

# サーバー設定
PORT = 5100
BIND_ADDRESS = "127.0.0.1"
ALLOW_LIST = ["127.0.0.1", "localhost", "::1"]

class ControlCenterHandler(http.server.SimpleHTTPRequestHandler):
    """管制塔ハンドラ：配信+統治機能"""
    
    def __init__(self, *args, **kwargs):
        # 配信ディレクトリを work_reports に限定
        reports = Cabinet.get_safe_path(
            "020_work_reports"
        )
        super().__init__(
            *args,
            directory=str(reports),
            **kwargs
        )

    def is_authorized(self):
        return self.client_address[0] in ALLOW_LIST

    def do_GET(self):
        if not self.is_authorized():
            self.send_error(403, "Forbidden")
            return
        
        # 特殊なエンドポイント：システムの健康状態を返す
        if self.path == "/api/status":
            self.send_status()
            return
            
        super().do_GET()

    def send_status(self):
        """与党としての「現況報告」API"""
        status_data = {
            "system": "100_gemini",
            "status": "Healthy",
            "time": datetime.now().isoformat(),
            "standard_version": "v3.2",
            "governance_root": str(Cabinet.root)
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(status_data).encode())

    def do_POST(self):
        if not self.is_authorized():
            self.send_error(403, "Forbidden")
            return

        # シャットダウン命令（認証付き）
        if self.path == "/api/shutdown":
            if self.headers.get("X-STP-Request") == "true":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Tower shutting down...")
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                self.send_error(401, "Unauthorized")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # ログは静かに（必要なら専用ファイルへ）
        pass

def start_tower():
    socketserver.TCPServer.allow_reuse_address = True
    addr = (BIND_ADDRESS, PORT)
    with socketserver.TCPServer(
        addr, ControlCenterHandler
    ) as httpd:
        print(f"--- 100_gemini Control Tower ---")
        print(f"Address: http://{BIND_ADDRESS}:{PORT}")
        print(f"Governance Root: {Cabinet.root}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nTower stopped.")

if __name__ == "__main__":
    start_tower()
