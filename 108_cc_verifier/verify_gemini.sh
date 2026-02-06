#!/bin/bash
# verify_gemini.sh
# CC検証（Geminiレポート照合）

set -euo pipefail

# 定数
readonly GEMINI_REPORT="${1:-}"
readonly EVIDENCE_DIR="${2:-}"
readonly TARGET_DIR="${3:-}"

# 引数チェック
if [[ -z "$GEMINI_REPORT" ]] || \
   [[ -z "$EVIDENCE_DIR" ]] || \
   [[ -z "$TARGET_DIR" ]]; then
    echo "使い方: $0 <Geminiレポート> <証跡DIR> <対象DIR>"
    exit 1
fi

# CC実証（wc -l）
cc_verify_wc() {
    local target_dir="$1"

    echo "【CC検証】wc -l 再実行" >&2
    local max=$(find "$target_dir" -type f \
        \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
        -exec wc -l {} + | grep -v " total$" | \
        awk '{if ($1 > max) max = $1} END {print max}')
    echo "最大行数: ${max}行" >&2
    echo "$max"
}

# CC実証（awk）
cc_verify_awk() {
    local target_dir="$1"

    echo "【CC検証】awk 再実行" >&2
    local count=$(find "$target_dir" -type f \
        \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
        -exec awk 'length > 80' {} + | wc -l | tr -d ' ')
    echo "80文字超過行数: ${count}行" >&2
    echo "$count"
}

# Geminiレポート照合
compare_with_gemini() {
    local gemini_report="$1"
    local cc_max_lines="$2"
    local cc_over80="$3"

    echo ""
    echo "【Geminiレポート】"
    grep -A 5 "| 500行制約 |" "$gemini_report" 2>/dev/null || \
        echo "レポート形式不明"

    echo ""
    echo "【照合結果】"
    echo "CC実証: 最大${cc_max_lines}行 / 80文字超過${cc_over80}行"

    # 判定
    if [ "$cc_max_lines" -le 500 ]; then
        echo "✅ 500行制約: 合格（最大${cc_max_lines}行）"
    else
        echo "❌ 500行制約: 不合格（最大${cc_max_lines}行）"
    fi
}

# メイン
main() {
    echo "🔍 CC検証開始"
    echo "対象: $TARGET_DIR"
    echo ""

    local cc_max=$(cc_verify_wc "$TARGET_DIR")
    echo ""
    local cc_over80=$(cc_verify_awk "$TARGET_DIR")

    compare_with_gemini "$GEMINI_REPORT" "$cc_max" "$cc_over80"

    echo ""
    echo "✅ CC検証完了"
}

main
