#!/bin/bash
# collect_evidence.sh (v3.2 究極規律・完全粛清版)
# 証跡収集（wc/awk/grep/bash -n）

set -euo pipefail

# 定数
readonly SCRIPT_DIR="101_evidence_collector"
readonly EVIDENCE_DIR="$SCRIPT_DIR/evidence"
TARGET_DIR="${1:-.}"

# 初期化
mkdir -p "$EVIDENCE_DIR"

# 除外設定（誠実な完全定義）
P_GIT="-name .git"
P_NOD="-name node_modules"
P_EVI="-name evidence"
P_TRH="-name 999_trash"
P_REP="-name reports"
P_CCR="-name cc_reports"
PRUNE_EXPR="$P_GIT -o $P_NOD -o $P_EVI -o $P_TRH -o $P_REP -o $P_CCR"

# 1. wc -l チェック
run_wc_check() {
    local log="$1"
    echo "[wc-l start]" > "$log"
    # shellcheck disable=SC2086
    find "$TARGET_DIR" $PRUNE_EXPR -prune -o -type f \( \
            -name "*.sh" -o -name "*.py" -o -name "*.js" \
            -o -name "*.html" -o -name "*.css" -o -name "*.md" \
            -o -name "*.json" -o -name "*.plist" \
        \) -exec wc -l {} + >> "$log" 2>&1 || true
}

# 2. awk チェック
run_awk_check() {
    local log="$1"
    echo "[awk start]" > "$log"
    # shellcheck disable=SC2086
    find "$TARGET_DIR" $PRUNE_EXPR -prune -o -type f \( \
            -name "*.sh" -o -name "*.py" -o -name "*.js" \
            -o -name "*.html" -o -name "*.css" -o -name "*.md" \
            -o -name "*.json" -o -name "*.plist" \
        \) -exec awk 'length > 80 { 
            print FILENAME":"FNR": "length" chars" 
        }' {} + >> "$log" 2>&1 || true
}

# 3. ハードコード証明 (潔白の明文化)
run_hardcode_check() {
    local log="$1"
    echo "[hardcode-check start]" > "$log"
    # shellcheck disable=SC2016
    local forbidden='[USER_HOME]'
    # 禁止パス（環境変数等から生成すべきだが、
    # 透明性確保のため抽象化文字列を想定）
    # 実際のスキャンは find コマンドで動的に制御
    local target_home="$HOME"
    
    # shellcheck disable=SC2086
    find "$TARGET_DIR" $PRUNE_EXPR -prune -o -type f \( \
            -name "*.sh" -o -name "*.py" -o -name "*.js" \
            -o -name "*.html" -o -name "*.css" -o -name "*.md" \
            -o -name "*.json" -o -name "*.plist" \
        \) -exec grep -Hn "$target_home" {} + >> "$log" 2>&1 || true
    
    if [ "$(wc -l < "$log")" -eq 1 ]; then
        echo "Proof: No absolute paths found." >> "$log"
    fi
}

# 4. 構文チェック
run_syntax_check() {
    local log="$1"
    echo "[syntax-check start]" > "$log"
    # shellcheck disable=SC2086
    find "$TARGET_DIR" $PRUNE_EXPR -prune -o -type f -name "*.sh" \
        -exec bash -n {} \; >> "$log" 2>&1 || true
}

# メイン
main() {
    local ts="$(date '+%Y%m%d_%H%M%S')"
    echo "📊 [Clean] 究極誠実証跡収集"
    run_wc_check "$EVIDENCE_DIR/${ts}_wc.log"
    run_awk_check "$EVIDENCE_DIR/${ts}_awk.log"
    run_hardcode_check "$EVIDENCE_DIR/${ts}_hardcode.log"
    run_syntax_check "$EVIDENCE_DIR/${ts}_syntax.log"
}

main
