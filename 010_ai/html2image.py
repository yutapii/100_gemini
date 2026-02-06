#!/usr/bin/env python3
"""
html2image.py - HTML→画像変換（Chrome headless版）

使い方:
    python3 html2image.py input.html          # PNG出力
    python3 html2image.py http://localhost:5050/        # URL指定
    python3 html2image.py input.html --output out.png
    python3 html2image.py input.html --width 1280 --height 1800
    python3 html2image.py input.html --wait 3000        # JS待機時間(ms)

特徴:
    - Chrome headless でフルページスクリーンショット
    - JSの実行を待ってから撮影（--virtual-time-budget）
    - スクロール不要でページ全体を撮影
"""
import os
import sys
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# Chromeパスを動的解決（環境変数 → which → デフォルト）
CHROME_PATH = (
    os.getenv("CHROME_PATH") or
    shutil.which("google-chrome") or
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

if not os.path.exists(CHROME_PATH):
    raise FileNotFoundError("Google Chromeが見つかりません")


def validate_output_path(path):
    """出力パスのバリデーション（パストラバ対策）"""
    abs_path = os.path.abspath(path)
    allowed_prefixes = ["/tmp", str(Path.home())]
    if not any(abs_path.startswith(p) for p in allowed_prefixes):
        raise ValueError(f"出力パスが許可されていません: {path}")
    return abs_path

def html_to_image(url_or_path, output_path, width=1280,
                  height=1800, wait_ms=5000):
    """Chrome headlessでフルページスクリーンショット"""

    # ファイルパスの場合はfile://に変換
    if os.path.exists(url_or_path):
        abs_path = os.path.abspath(url_or_path)
        url = f"file://{abs_path}"
    else:
        url = url_or_path

    # Chrome headless コマンド
    cmd = [
        CHROME_PATH,
        "--headless",
        f"--screenshot={output_path}",
        f"--window-size={width},{height}",
        "--disable-gpu",
        f"--virtual-time-budget={wait_ms}",
        "--hide-scrollbars",
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(output_path):
        return output_path
    else:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="HTML→フルページ画像変換（Chrome headless）"
    )
    parser.add_argument("html", help="入力HTMLファイル or URL")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--width", type=int, default=1280,
                        help="幅（デフォルト: 1280）")
    parser.add_argument("--height", type=int, default=1800,
                        help="高さ（デフォルト: 1800）")
    parser.add_argument("--wait", type=int, default=5000,
                        help="JS待機時間ms（デフォルト: 5000）")
    args = parser.parse_args()

    # 出力パス決定（バリデーション済み）
    if args.output:
        output_path = validate_output_path(args.output)
    else:
        if args.html.startswith("http"):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = f"/tmp/screenshot_{timestamp}.png"
        else:
            base = os.path.splitext(args.html)[0]
            output_path = f"{base}.png"
            output_path = validate_output_path(output_path)

    result = html_to_image(
        args.html, output_path, args.width, args.height, args.wait
    )

    if result:
        print(result)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
