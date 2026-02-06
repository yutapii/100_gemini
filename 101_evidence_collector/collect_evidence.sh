#!/bin/bash
# collect_evidence.sh
# 証跡収集（wc/awk/grep/bash -n）

set -euo pipefail

# 定数
readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly EVIDENCE_DIR="$SCRIPT_DIR/evidence"
readonly TARGET_DIR="${1:-.}"

# 初期化
mkdir -p "$EVIDENCE_DIR"

# wc -l チェック
run_wc_check() {
    local target="$1"
    local log="$2"
    local ts="$(date '+%Y-%m-%d %H:%M:%S')"

    echo "[$ts] wc -l 実行開始" > "$log"
    if find "$target" -type f \
        \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
        -exec wc -l {} + | grep -v " total$" >> "$log" 2>&1; then
        echo "[$ts] wc -l 実行成功" >> "$log"
        return 0
    else
        echo "[$ts] wc -l 実行失敗" >> "$log"
        return 1
    fi
}

# awk チェック（80文字超過）
run_awk_check() {
    local target="$1"
    local log="$2"
    local ts="$(date '+%Y-%m-%d %H:%M:%S')"

    echo "[$ts] awk実行開始" > "$log"
    if find "$target" -type f \
        \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
        -exec awk 'length > 80 {
            print FILENAME":"NR":"length": "substr($0,1,60)"..."
        }' {} + >> "$log" 2>&1; then
        echo "[$ts] awk実行成功" >> "$log"
        return 0
    else
        echo "[$ts] awk実行失敗" >> "$log"
        return 1
    fi
}

# grep チェック（機密情報）
run_grep_check() {
    local target="$1"
    local log="$2"
    local ts="$(date '+%Y-%m-%d %H:%M:%S')"

    echo "[$ts] grep実行開始" > "$log"
    if find "$target" -type f \
        \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) \
        -exec grep -Hn \
        -e "password\s*=" \
        -e "api_key\s*=" \
        -e "secret\s*=" \
        {} + >> "$log" 2>&1; then
        echo "[$ts] grep実行成功（検出あり）" >> "$log"
    else
        echo "[$ts] grep実行成功（検出なし）" >> "$log"
    fi
    return 0
}

# bash -n チェック（構文）
run_syntax_check() {
    local target="$1"
    local log="$2"
    local ts="$(date '+%Y-%m-%d %H:%M:%S')"

    echo "[$ts] 構文チェック開始" > "$log"

    # bash
    find "$target" -name "*.sh" -type f | while read -r f; do
        if bash -n "$f" 2>&1 | tee -a "$log"; then
            echo "[$ts] ✅ $f" >> "$log"
        else
            echo "[$ts] ❌ $f" >> "$log"
        fi
    done

    # python
    find "$target" -name "*.py" -type f | while read -r f; do
        if python3 -m py_compile "$f" 2>&1 | tee -a "$log"; then
            echo "[$ts] ✅ $f" >> "$log"
        else
            echo "[$ts] ❌ $f" >> "$log"
        fi
    done

    return 0
}

# メイン
main() {
    local target="$1"
    local timestamp="$(date '+%Y%m%d_%H%M%S')"

    echo ""
    echo "📊 証跡収集開始"
    echo "対象: $target"
    echo ""

    run_wc_check "$target" \
        "$EVIDENCE_DIR/${timestamp}_wc.log"
    run_awk_check "$target" \
        "$EVIDENCE_DIR/${timestamp}_awk.log"
    run_grep_check "$target" \
        "$EVIDENCE_DIR/${timestamp}_grep.log"
    run_syntax_check "$target" \
        "$EVIDENCE_DIR/${timestamp}_syntax.log"

    echo ""
    echo "✅ 証跡収集完了"
    echo "保存先: $EVIDENCE_DIR/${timestamp}_*.log"
}

# 実行
main "$TARGET_DIR"
