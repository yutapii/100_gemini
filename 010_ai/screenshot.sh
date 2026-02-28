#!/bin/bash
# screenshot.sh (v3.5 Iron Gate Edition)
# 100_Gemini 目玉機能：視覚的証跡収集

set -euo pipefail

# === 定義 ===
S_DIR="010_ai"
PY_SCRIPT="$S_DIR/screenshot.py"
OUT_DIR="$S_DIR/screenshots"
PORT=5100
URL="http://localhost:$PORT/"

# === 引数処理 ===
TARGET="${1:-main}"
MODE="${2:-half}" # tiny / half / full

OUT_FILE="$OUT_DIR/latest_${TARGET}_${MODE}.png"

# === 執行 ===
echo "📸 Capture: $URL ($MODE) -> $OUT_FILE"

# python3 screenshot.py [URL] [Path] [Mode]
# 80文字制限遵守のため分割して実行
python3 "$PY_SCRIPT" 
    "$URL" 
    "$OUT_FILE" 
    "$MODE"

echo "✅ Saved: $OUT_FILE"
