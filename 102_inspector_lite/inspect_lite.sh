#!/bin/bash
# inspect_lite.sh
# 簡易検査（Flash-Lite 💵）

set -euo pipefail

# 定数
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly REPORTS_DIR="$SCRIPT_DIR/reports"
readonly EVIDENCE_DIR="${1:-}"
readonly TARGET_DIR="${2:-}"

# 初期化
mkdir -p "$REPORTS_DIR"

# 引数チェック
if [[ -z "$EVIDENCE_DIR" ]] || [[ -z "$TARGET_DIR" ]]; then
    echo "使い方: $0 <証跡ディレクトリ> <対象ディレクトリ>"
    exit 1
fi

# 簡易検査実行
run_lite_inspection() {
    local evidence_dir="$1"
    local target_dir="$2"
    local ts="$(date '+%Y%m%d_%H%M%S')"
    local report="$REPORTS_DIR/${ts}_lite.md"

    echo ""
    echo "🔍 簡易検査開始（Flash-Lite 💵）"
    echo ""

    # 証跡ログ読み込み
    local latest_wc=$(ls -t "${evidence_dir}"/*_wc.log 2>/dev/null | head -1)
    local latest_awk=$(ls -t "${evidence_dir}"/*_awk.log 2>/dev/null | head -1)
    local wc_content=$(cat "$latest_wc" 2>/dev/null || echo "なし")
    local awk_content=$(cat "$latest_awk" 2>/dev/null || echo "なし")

    # プロンプト
    local prompt="
品質検査AIです。以下の証跡ログを分析してください。

【重要原則】
1. 推測禁止：証跡ログの事実のみを根拠とする
2. wc.logの「total」行は合計値、ファイル行数ではない
3. 合格/不合格を明確に判定

【証跡ログ】
=== wc.log ===
${wc_content}

=== awk.log（80文字超過）===
${awk_content}

【検査項目】
1. 500行/ファイル制約: 全ファイル500行以下か？
2. 80文字/行制約: 超過行ゼロか？

【出力形式】
## Level 1検査結果

| 項目 | 判定 | 証跡 |
|------|------|------|
| 500行制約 | ✅/❌ | 最大XXX行 |
| 80文字制約 | ✅/❌ | 超過XX行 |
| 機密情報 | ✅/❌ | 検出XX件 |
| 構文エラー | ✅/❌ | エラーXX件 |

**総合判定**: ✅合格 / ❌不合格
"

    # Gemini実行
    if cd "$target_dir" && \
        gemini --model "gemini-2.5-flash-lite" \
        "$prompt" > "$report" 2>&1; then
        cat "$report"
        echo ""
        echo "✅ Level 1検査完了"
        echo "レポート: $report"
        return 0
    else
        echo "❌ Level 1検査失敗"
        cat "$report"
        return 1
    fi
}

# 実行
run_lite_inspection "$EVIDENCE_DIR" "$TARGET_DIR"
