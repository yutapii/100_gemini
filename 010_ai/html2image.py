import os
import sys
import subprocess
from path_utils import get_safe_path

def convert_html_to_image(html_path, output_path):
    """
    HTMLファイルを画像に変換する
    """
    try:
        # 厳格なディレクトリチェック（脆弱性修正）
        abs_html = get_safe_path(html_path)
        abs_output = get_safe_path(output_path)
        
        print(f"Converting {abs_html} to {abs_output}")
        # 外部コマンド実行（モック）
        return True
    except Exception as e:
        print(f"Security Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python html2image.py <html_path> <output_path>")
        sys.exit(1)
    convert_html_to_image(sys.argv[1], sys.argv[2])
