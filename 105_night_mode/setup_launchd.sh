#!/bin/bash
# setup_launchd.sh
# macOS Launchd setup for nightly inspection

set -euo pipefail

# スクリプトの絶対パスをベースにする
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLIST_NAME="com.gemini.inspection.nightly.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"

# ... (Setup logic)

# 警告されたパス依存のテスト機能を修正
run_test() {
    echo "Testing nightly inspection..."
    # ハードコードをやめ、BASE_DIR を使用
    if [ -f "$BASE_DIR/inspect.sh" ]; then
        "$BASE_DIR/inspect.sh" "$BASE_DIR"
    else
        echo "Error: inspect.sh not found in $BASE_DIR"
        exit 1
    fi
}

if [[ "${1:-}" == "--test" ]]; then
    run_test
fi
