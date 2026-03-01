#!/bin/bash
# inspect_v3_iron_gate.sh
# 100_Gemini 鋼鉄の関門 (V3.5 Semantic & Asset Excellence)
# 規律・セキュリティ・メンテナンス性・成長性 統合検査

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
echo "## 鋼鉄の関門 (V3.5) 検査レポート"
echo "**対象**: $TARGET_DIR"
echo "**実施日時**: $(date '+%Y-%m-%d %H:%M')"
GATE="$SCRIPT_DIR/../083_quality_inspection"
echo "**規律基準**: [IRON_GATE_V3.5.md]($GATE/IRON_GATE_V3.5.md)"
echo ""
echo "### 5 Whys 思考プロセス（TPS）"
echo "1. なぜ肥大化したのか？"
echo "2. なぜそこに居座るのか？"
echo "3. なぜその構造（セマンティクス）か？"
echo "4. なぜ他者が理解できるのか？"
echo "5. なぜ今、是正が必要なのか？"
echo ""
} > "$REPORT_FILE"

# === 1. 規律検査 (450行警告 / 500行上限 / 80文字) ===
{
echo "### 1. 規律遵守状況 (成長性・可読性)"
echo "| ファイル | 行数 | 80文字超 | 判定 | 備考 |"
echo "| :--- | :---: | :---: | :---: | :--- |"
} >> "$REPORT_FILE"

find "$TARGET_DIR" -type f \
    \( -name "*.py" -o -name "*.js" \
       -o -name "*.sh" -o -name "*.md" \
       -o -name "*.html" \) \
    -not -path "*/.git/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/999_trash/*" \
    -not -path "*/venv/*" \
    -not -path "*/.venv/*" \
    -not -path "*/site-packages/*" \
  | while read -r file; do

    lc=$(wc -l < "$file" | xargs)
    ll=$(awk 'length($0) > 80' "$file" | wc -l | xargs)

    status="✅"
    note="良好"
    
    if [ "$lc" -gt 450 ]; then
        status="⚠️"
        note="成長警告（論理分割の検討要）"
    fi
    if [ "$lc" -gt 500 ]; then
        status="❌"
        note="規律違反（物理分割必須）"
    fi
    if [ "$ll" -gt 0 ]; then
        status="❌"
        note="80文字超過（可読性欠如）"
    fi

    fname=$(basename "$file")
    echo "| $fname | $lc | $ll | $status | $note |" \
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

# === 3. セマンティクス・メンテナンス性 ===
echo "### 3. セマンティクス・構造" >> "$REPORT_FILE"

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
    echo "**判定: 不適合 (改善が必要)**" \
        >> "$REPORT_FILE"
elif grep -q "⚠️" "$REPORT_FILE"; then
    echo "**判定: 適合 (成長警告あり・Kaizen継続)**" \
        >> "$REPORT_FILE"
else
    echo "**判定: 適合 (Kaizen継続)**" \
        >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"
echo "Gemini🔍 (鋼鉄の関門 V3.5)" >> "$REPORT_FILE"

echo "✅ 検査完了: $REPORT_FILE"
