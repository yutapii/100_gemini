#!/bin/bash
# Gemini API自動リトライスクリプト（クォータ復活待機）

set -euo pipefail

# 設定
MAX_RETRIES=5
WAIT_TIME=60  # RPM/TPMは60秒でリセット
TARGET_DIR="${1:-.}"
INSPECTION_PROMPT="${2:-品質検査を実行してください}"
MODEL="${3:-gemini-2.5-flash-lite}"  # デフォルトはFlash-Lite

echo "-----------------------------------------"
echo "Gemini自動リトライ検査"
echo "-----------------------------------------"
echo "対象: $TARGET_DIR"
echo "モデル: $MODEL"
echo "最大リトライ: $MAX_RETRIES回"
echo "-----------------------------------------"
echo ""

attempt=1

while [ $attempt -le $MAX_RETRIES ]; do
    echo "🔄 試行 $attempt/$MAX_RETRIES..."
    echo "実行: cd $TARGET_DIR && \\"
    echo "      gemini --model $MODEL \"$INSPECTION_PROMPT\""
    echo ""

    # Gemini実行（エラーをキャプチャ）
    if output=$(cd "$TARGET_DIR" && \
            gemini --model "$MODEL" "$INSPECTION_PROMPT" 2>&1); then
        echo "✅ 検査成功！"
        echo "$output"
        exit 0
    else
        # エラーメッセージを確認
        if echo "$output" | grep -q "429\|RESOURCE_EXHAUSTED\|capacity"; then
            echo "⚠️ API容量制限（429エラー）"

            # RPM/TPM制限と判定
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "💤 ${WAIT_TIME}秒待機してリトライ..."
                echo "（クォータは60秒でリセット）"
                echo ""

                # カウントダウン表示
                for ((i=WAIT_TIME; i>0; i-=10)); do
                    echo "   残り ${i}秒..."
                    sleep 10
                done

                ((attempt++))
            else
                echo "❌ 最大リトライ回数に達しました"
                echo ""
                echo "【原因】RPD（1日クォータ）制限の可能性"
                echo "【対策】"
                echo "  1. 翌日午前0時（太平洋時間）まで待つ"
                echo "  2. モデルを変更（Flash-Lite → Flash → Pro）"
                echo "  3. Google Cloud Consoleでクォータ確認"
                exit 1
            fi
        else
            # 429以外のエラー
            echo "❌ エラー発生（429以外）"
            echo "$output"
            exit 1
        fi
    fi
done

echo "❌ リトライ失敗"
exit 1
