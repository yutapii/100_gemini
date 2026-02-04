#!/usr/bin/env python3
"""
100_Gemini Server
ポート5100で静的ファイル配信 + API
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys
import signal
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# === 設定 ===
PROJECT_ROOT = "/Users/saitoyutaka/100_gemini"
PORT = 5100
SYSTEM_NAME = "Gemini CLI"
SIGTERM_LOG_FILE = Path(__file__).parent / "sigterm.log"


def sigterm_handler(signum, frame):
    """SIGTERMシグナル受信時のログ記録"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pid = os.getpid()
    ppid = os.getppid()

    parent_info = "unknown"
    try:
        ps_result = subprocess.run(
            ["ps", "-p", str(ppid), "-o", "comm=,args="],
            capture_output=True, text=True, timeout=2
        )
        if ps_result.stdout.strip():
            parent_info = ps_result.stdout.strip()
    except Exception:
        pass

    log_msg = f"""
{'='*60}
SIGTERM受信! ゴースト停止発生
{'='*60}
時刻: {timestamp}
PID: {pid}
親PID: {ppid}
親プロセス: {parent_info}
シグナル: {signum}
{'='*60}
"""
    with open(SIGTERM_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg)
    print(log_msg, file=sys.stderr)
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)


class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def _set_json_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            self._handle_health()
        elif self.path == '/api/shutdown':
            self._handle_shutdown()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/shutdown':
            self._handle_shutdown()
        else:
            self._set_json_headers(404)
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode())

    def _handle_health(self):
        self._set_json_headers(200)
        response = {
            'status': 'ok',
            'service': SYSTEM_NAME,
            'port': PORT
        }
        self.wfile.write(json.dumps(response).encode())

    def _handle_shutdown(self):
        # X-STP-Request ヘッダーチェック（必須）
        stp_request = self.headers.get('X-STP-Request', '')
        if stp_request != 'true':
            self._set_json_headers(401)
            response = {'error': 'Unauthorized'}
            self.wfile.write(json.dumps(response).encode())
            return

        self._set_json_headers(200)
        response = {'success': True, 'message': f'{SYSTEM_NAME}停止'}
        self.wfile.write(json.dumps(response).encode())
        threading.Thread(target=lambda: os._exit(0)).start()


def run_server():
    httpd = HTTPServer(('', PORT), CustomHandler)
    print(f"🚀 {SYSTEM_NAME} Server on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
