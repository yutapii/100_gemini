#!/usr/bin/env python3
"""
OAuth中継サーバー
認証コードを自動取得してクリップボードにコピー
"""
import argparse
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def copy_to_clipboard(text):
    """クリップボードにコピー（macOS）"""
    try:
        subprocess.run(
            ['pbcopy'],
            input=text.encode('utf-8'),
            check=True
        )
        print("クリップボードにコピーしました")
    except Exception as e:
        print(f"クリップボードコピー失敗: {e}")


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """OAuth callbackを受け取るハンドラー"""

    def log_message(self, format, *args):
        """ログ出力を抑制"""
        pass

    def do_GET(self):
        """GETリクエスト処理"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if 'code' in params:
            code = params['code'][0]
            print(f"\n認証コード取得:\n{code}\n")
            copy_to_clipboard(code)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html><body style="font-family:sans-serif;
                text-align:center;padding:50px;">
                <h1>OK</h1>
                <p>Code copied to clipboard!</p>
                <p>Close this window and return to terminal.</p>
                </body></html>
            """)

            self.server.shutdown_requested = True
        else:
            self.send_response(400)
            self.end_headers()


def run_server(port=8080):
    """中継サーバー起動"""
    server = HTTPServer(('localhost', port), OAuthCallbackHandler)
    server.shutdown_requested = False

    print(f"OAuth中継サーバー起動: http://localhost:{port}")
    print("認証後、自動的に停止します...\n")

    while not server.shutdown_requested:
        server.handle_request()

    print("サーバー停止")


def main():
    parser = argparse.ArgumentParser(
        description='OAuth中継サーバー'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='ポート番号（デフォルト: 8080）'
    )

    args = parser.parse_args()
    run_server(args.port)


if __name__ == '__main__':
    main()
