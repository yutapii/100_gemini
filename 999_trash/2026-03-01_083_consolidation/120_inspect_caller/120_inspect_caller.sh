#!/bin/bash
# 120_inspect_caller.sh
# 役割:Facts + Issue log をGemini CLIに渡す

# ---- 設定 ----
# PATH から gemini を検索。
GEMINI_BIN=$(which gemini)
if [ -z "$GEMINI_BIN" ]; then
    # 80文字制限遵守のため分割
    FALLBACK_PATH="$HOME/001_npm-global/bin/gemini"
    GEMINI_BIN="$FALLBACK_PATH"
fi

DIR="$(dirname "$0")"
FACTS="${DIR}/../121_project_facts/121_project_facts.md"
LOG="${DIR}/../122_issue_log/122_issue_log.md"
TMP="/tmp/120_inspect_$(date +%s).txt"

# ---- 証跡前置き ----
echo "# ===== 検査コンテキスト =====" > "$TMP"
[ -f "$FACTS" ] && cat "$FACTS" >> "$TMP"
[ -f "$LOG" ] && cat "$LOG" >> "$TMP"
echo "# ===== 今回の検査依頼 =====" >> "$TMP"

# ---- パイプ入力 ----
[ ! -t 0 ] && cat >> "$TMP"

# ---- Gemini実行 ----
cat "$TMP" | "$GEMINI_BIN" -y

# ---- 後片付け ----
rm -f "$TMP"
