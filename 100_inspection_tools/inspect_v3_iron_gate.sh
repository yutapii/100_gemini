#!/bin/bash
# inspect_v3_iron_gate.sh
# 100_Gemini 鋼鉄の関門 (v3.2)
# 規律・セキュリティ・メンテナンス性 統合検査

set -euo pipefail

# === 定義 ===
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
readonly SCRIPT_DIR
readonly TARGET_DIR="${1:-.}"
readonly EVIDENCE_DIR="$SCRIPT_DIR/evidence"
TS=$(date +%Y%m%d_%H%M%S)
RDIR="$SCRIPT_DIR/reports"
readonly REPORT_FILE="$RDIR/inspection_report_${TS}.md"

# === 0. 準備 ===
mkdir -p "$EVIDENCE_DIR" "$RDIR"

{
echo "## 鋼鉄の関門 (v3.2) 検査レポート"
echo "**対象**: $TARGET_DIR"
echo "**実施日時**: $(date '+%Y-%m-%d %H:%M')"
echo ""
} > "$REPORT_FILE"

# === 1. 規律検査 (500行 / 80文字) ===
{
echo "### 1. 規律遵守状況"
echo "| ファイル | 行数 | 80文字超 | 判定 |"
echo "| :--- | :---: | :---: | :---: |"
} >> "$REPORT_FILE"

EXCL="-not -path */.*"
EXCL="$EXCL -not -path */node_modules/*"
EXCL="$EXCL -not -path */999_trash/*"

find "$TARGET_DIR" -type f \
    \( -name "*.py" -o -name "*.js" -o -name "*.sh" \) \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/999_trash/*" \
  | while read -r file; do

    lc=$(wc -l < "$file" | xargs)
    ll=$(awk 'length($0) > 80' "$file" | wc -l | xargs)

    status="✅"
    if [ "$lc" -gt 500 ] || [ "$ll" -gt 0 ]; then
        status="❌"
    fi

    fname=$(basename "$file")
    echo "| $fname | $lc | $ll | $status |" \
        >> "$REPORT_FILE"
done
echo "" >> "$REPORT_FILE"

# === 2. セキュリティ検査 ===
{
echo "### 2. セキュリティ・機密性"
echo "| 項目 | 状態 | 詳細 |"
echo "| :--- | :---: | :--- |"
} >> "$REPORT_FILE"

GI="$TARGET_DIR/.gitignore"
if grep -q "040_security" "$GI" 2>/dev/null; then
    echo "| .gitignore | ✅ | 040_security除外済 |" \
        >> "$REPORT_FILE"
else
    echo "| .gitignore | ❌ | 040_security未除外 |" \
        >> "$REPORT_FILE"
fi

EXCL_DIRS="{.git,040_security,999_trash}"
EXCL_DIRS="$EXCL_DIRS,{node_modules,__pycache__}"
secret_found=$(grep -rE \
    "password|api_key|secret|token" \
    "$TARGET_DIR" \
    --exclude-dir=.git \
    --exclude-dir=040_security \
    --exclude-dir=999_trash \
    --exclude-dir=node_modules \
    --exclude-dir=__pycache__ \
    --exclude="*.md" 2>/dev/null \
  | wc -l | xargs)

if [ "$secret_found" -eq 0 ]; then
    echo "| 秘密情報 | ✅ | ハードコードなし |" \
        >> "$REPORT_FILE"
else
    msg="$secret_found 件検出（要目視確認）"
    echo "| 秘密情報 | ⚠️ | $msg |" \
        >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# === 3. メンテナンス性 ===
echo "### 3. メンテナンス性・構造" >> "$REPORT_FILE"

fc=$(find "$TARGET_DIR" -maxdepth 1 \
    -type d -name "[0-9][0-9][0-9]_*" \
  | wc -l | xargs)
echo "- **機能フォルダ数**: $fc" >> "$REPORT_FILE"

if find "$TARGET_DIR" -name "config" \
    -type d | grep -q "."; then
    echo "- **設定分離**: ✅ 確認済" \
        >> "$REPORT_FILE"
else
    echo "- **設定分離**: ⚠️ 要確認" \
        >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# === 最終判定 ===
{
echo "---"
echo "### 最終判定"
} >> "$REPORT_FILE"

if grep -q "❌" "$REPORT_FILE"; then
    echo "**判定: 不合格 (再検査が必要)**" \
        >> "$REPORT_FILE"
else
    echo "**判定: 合格 (100点)**" \
        >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"
echo "Gemini🔍 (鋼鉄の関門 v3.2)" >> "$REPORT_FILE"

echo "✅ 検査完了: $REPORT_FILE"
