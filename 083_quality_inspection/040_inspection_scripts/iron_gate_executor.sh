#!/bin/bash
# 083_quality_inspection/040_inspection_scripts/iron_gate_executor.sh
# 鋼鉄の関門：物理執行スクリプト

TARGET_DIR=$1
if [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 <target_directory>"
    exit 1
fi

echo "=== [Physical Execution] 物理証跡検査開始: $TARGET_DIR ==="

# 1. 物理実在と指紋(MD5)の取得
echo "[1/3] ファイル実在・ハッシュ確認"
find "$TARGET_DIR" -maxdepth 2 -type f -not -path '*/.*' | while read f; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
        md5 -r "$f"
    else
        md5sum "$f"
    fi
done

# 2. 動的構文チェック (Pythonの場合)
echo "[2/3] 動的構文チェック (python3 -m py_compile)"
find "$TARGET_DIR" -maxdepth 2 -name "*.py" | while read py; do
    python3 -m py_compile "$py"
    if [ $? -eq 0 ]; then
        echo "✅ OK: $py"
    else
        echo "❌ FAIL: $py"
        exit 1
    fi
done

# 3. 規律遵守チェック (80文字制限)
echo "[3/3] 規律遵守チェック (80文字制限)"
TARGETS=$(find "$TARGET_DIR" -maxdepth 2 \
  -type f -not -path '*/.*' \
  \( -name "*.py" -o -name "*.js" \
     -o -name "*.md" \))
LONG_LINES=$(awk \
  'length > 80 {print FILENAME ":" FNR}' \
  $TARGETS)
if [ -z "$LONG_LINES" ]; then
    echo "✅ OK: 全行80文字以内"
else
    echo "❌ FAIL: 80文字超過検出"
    echo "$LONG_LINES"
    exit 1
fi

echo "=== 物理執行完了 ==="
echo "合格判定: 正常系PASS"
echo "※ 100点を達成するには異常系・破壊テストの追加証跡を示せ"
