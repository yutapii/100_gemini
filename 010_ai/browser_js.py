#!/usr/bin/env python3
"""
browser_js.py - ブラウザでJavaScript実行（コード目）

使い方:
    python3 browser_js.py "document.title"
    python3 browser_js.py "document.querySelectorAll('h2').length"
    python3 browser_js.py --file script.js
"""
import sys
import argparse
import subprocess
from pathlib import Path

# セキュリティ: JSファイルは特定ディレクトリのみ許可
ALLOWED_JS_DIR = Path.home() / "100_gemini/010_ai/safe_scripts"

def validate_js_file(filepath):
    """JSパスのバリデーション（パストラバーサル対策）"""
    path = Path(filepath).resolve()
    if not path.is_relative_to(ALLOWED_JS_DIR):
        raise ValueError(
            f"JSファイルが許可されたディレクトリ外: {filepath}"
        )
    if not path.exists():
        raise FileNotFoundError(
            f"JSファイルが見つかりません: {filepath}"
        )
    return path


def run_js_chrome(js_code):
    """ChromeでJavaScript実行

    注意: 外部JSは危険。信頼できるファイルのみ使用
    """
    script = f'''
    tell application "Google Chrome"
        tell active tab of front window
            execute javascript "{js_code}"
        end tell
    end tell
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="ブラウザJS実行")
    parser.add_argument("code", nargs="?", help="実行するJSコード")
    parser.add_argument("--file", "-f", help="JSファイル")
    args = parser.parse_args()

    if args.file:
        validated_path = validate_js_file(args.file)
        with open(validated_path, "r") as f:
            js_code = f.read().replace('"', '\\"').replace('\n', ' ')
    elif args.code:
        js_code = args.code.replace('"', '\\"')
    else:
        print("Error: code or --file required", file=sys.stderr)
        sys.exit(1)

    result = run_js_chrome(js_code)
    print(result)

if __name__ == "__main__":
    main()
