import sys
import os
import subprocess
from path_utils import get_safe_path

def take_screenshot(url, output_path, mode="half"):
    """
    Take a screenshot with specific resolution (tiny/half/full)
    """
    res = {"tiny": (320, 480), "half": (640, 960), "full": (1280, 1920)}
    w, h = res.get(mode, res["half"])
    
    try:
        # 共通バリデーション
        abs_output = get_safe_path(output_path)
        
        # 80文字制限遵守のため AppleScript を分割定義
        script = (
            'tell application "Safari"\n'
            f'  make new document with properties {{URL:"{url}"}}\n'
            '  delay 3\n'
            f'  set bounds of window 1 to {{0, 0, {w}, {h}}}\n'
            'end tell\n'
            'delay 1\n'
            f'do shell script "screencapture -x {abs_output}"'
        )
        
        subprocess.run(["osascript", "-e", script], check=True)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python screenshot.py [URL] [Path] [Mode]")
        sys.exit(1)
    
    m = sys.argv[3] if len(sys.argv) > 3 else "half"
    take_screenshot(sys.argv[1], sys.argv[2], m)
