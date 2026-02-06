#!/usr/bin/env python3
"""
screenshot.py - スクリーンショット取得

使い方:
    python3 screenshot.py                    # メインモニタ全体
    python3 screenshot.py --url https://...  # URL指定
    python3 screenshot.py --output out.png   # 出力先指定
"""
import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def validate_output_path(path):
    """出力パスのバリデーション
    （パストラバーサル対策）"""
    abs_path = os.path.abspath(path)
    allowed_prefixes = ["/tmp", str(Path.home())]
    if not any(abs_path.startswith(p) for p in allowed_prefixes):
        raise ValueError(f"出力パスが許可されていません: {path}")
    return abs_path

def screenshot_screen(output_path):
    """画面全体をキャプチャ（macOS screencapture）"""
    subprocess.run(["screencapture", "-x", output_path], check=True)
    return output_path

def screenshot_url(url, output_path):
    """URLをChromeで開いてキャプチャ"""
    script = f'''
    tell application "Google Chrome"
        activate
        open location "{url}"
        delay 2
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)
    subprocess.run(["screencapture", "-x", output_path], check=True)
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="スクリーンショット取得"
    )
    parser.add_argument("--url", help="キャプチャするURL")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    args = parser.parse_args()

    if args.output:
        output_path = validate_output_path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"/tmp/screenshot_{timestamp}.png"

    if args.url:
        result = screenshot_url(args.url, output_path)
    else:
        result = screenshot_screen(output_path)

    print(result)

if __name__ == "__main__":
    main()
