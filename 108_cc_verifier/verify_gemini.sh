#!/bin/bash
# verify_gemini.sh
# Geminiの出力を検証する（除外設定同期版）

set -euo pipefail

TARGET_DIR="${1:-.}"
# 除外設定（さらに短く改行して80文字制限遵守）
PRUNE_ARGS="-name .git -o -name node_modules -o -name __pycache__ \
-o -name evidence -o -name reports -o -name 999_trash"

echo "Verifying $TARGET_DIR..."

# 共通の除外リストを適用して検索
# shellcheck disable=SC2086
find "$TARGET_DIR" \( $PRUNE_ARGS \) -prune -o -type f \
    \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) -print | \
    while read -r f; do
    echo "Checking $f..."
    # Verification logic...
done
