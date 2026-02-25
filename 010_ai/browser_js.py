import sys
import subprocess
from path_utils import get_safe_path

def execute_browser_js(url, js_code):
    """
    Execute JavaScript in Safari via AppleScript (Secure version)
    """
    try:
        # URLのバリデーション（簡易）
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL")

        applescript = """
        on run {target_url, target_js}
            tell application "Safari"
                if (count of documents) is 0 then
                    make new document with properties {URL:target_url}
                    delay 2
                end if
                do JavaScript target_js in document 1
            end tell
        end run
        """
        subprocess.run([
            "osascript", "-e", applescript, url, js_code
        ], check=True)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    execute_browser_js(sys.argv[1], sys.argv[2])
