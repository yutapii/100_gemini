#!/bin/bash
# 100_gemini 統合検査コマンド（v3.2 確定版）
# 使い方: ./inspect.sh [対象ディレクトリ]

set -euo pipefail

TARGET="${1:-.}"
# 相対パス計算
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$BASE_DIR/107_orchestrator/run_inspection.sh"

# 100番地の統合制御を呼び出す
"$SCRIPT" "$TARGET"
