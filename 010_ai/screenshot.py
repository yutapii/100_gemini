import sys
import os
import subprocess
from path_utils import get_safe_path

def take_screenshot(url, output_path):
    """
    Take a screenshot using Safari via AppleScript (Secure version)
    """
    try:
        # 共通バリデーション適用
        abs_output = get_safe_path(output_path)
        
        applescript = """
        on run {target_url, target_path}
            tell application "Safari"
                make new document with properties {URL:target_url}
                delay 2
            end tell
        end run
        """
        subprocess.run([
            "osascript", "-e", applescript, url, str(abs_output)
        ], check=True)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    take_screenshot(sys.argv[1], sys.argv[2])
