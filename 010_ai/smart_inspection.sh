#!/bin/bash
# スマート品質検査（3段階エスカレーション+自動リトライ）

set -euo pipefail

TARGET_DIR="${1:-.}"
RETRY_WAIT=60  # RPM/TPMリセット時間

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 スマート品質検査（3段階エスカレーション）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "対象: $TARGET_DIR"
echo "戦略: 簡易 → 中程度 → 精密"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Gemini実行（リトライ付き）
run_gemini_with_retry() {
    local model=$1
    local prompt=$2
    local max_retries=3
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        echo "🔄 試行 $attempt/$max_retries (モデル: $model)..."

        if output=$(cd "$TARGET_DIR" && gemini --model "$model" "$prompt" 2>&1); then
            echo "$output"
            return 0
        else
            if echo "$output" | grep -q "429\|RESOURCE_EXHAUSTED\|capacity"; then
                if [ $attempt -lt $max_retries ]; then
                    echo "⚠️ 429エラー - ${RETRY_WAIT}秒待機..."
                    sleep $RETRY_WAIT
                    ((attempt++))
                else
                    return 1
                fi
            else
                echo "$output"
                return 1
            fi
        fi
    done
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レベル1：簡易検査（Flash-Lite）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "【レベル1：簡易検査】Flash-Lite 💵"
echo "検査項目: 必須4項目（500行, 80文字, 機密情報, 構文エラー）"
echo ""

PROMPT_L1="以下の項目を検査してください：
1. 500行/ファイル制約（wc -l実行）
2. 80文字/行制約（awk実行）
3. 機密情報漏洩（grep実行）
4. 構文エラー

【重要】推測禁止、必ずコマンド実行結果を記録。
合格/不合格を明確に判定してください。"

if run_gemini_with_retry "gemini-2.5-flash-lite" "$PROMPT_L1"; then
    echo ""
    echo "✅ レベル1で合格の可能性"
    echo "💰 コスト: 💵（最安）"
    echo ""
    echo "次のステップ: Claude Code再点検を実行してください"
    exit 0
else
    echo ""
    echo "⚠️ レベル1不合格 or API制限"
    echo "→ レベル2へエスカレーション"
    echo ""
    sleep 5
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レベル2：中程度検査（Flash）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "【レベル2：中程度検査】Flash 💵💵"
echo "検査項目: 必須5+重要4項目"
echo ""

PROMPT_L2="以下の項目を検査してください：
【必須】500行, 80文字, XSS, 機密情報, 構文エラー
【重要】セマンティックHTML, グローバル変数, コード重複, a11y

【重要】推測禁止、必ずコマンド実行結果を記録。
合格/不合格を明確に判定してください。"

if run_gemini_with_retry "gemini-2.5-flash" "$PROMPT_L2"; then
    echo ""
    echo "✅ レベル2で合格の可能性"
    echo "💰 コスト: 💵💵💵（中）"
    echo ""
    echo "次のステップ: Claude Code再点検を実行してください"
    exit 0
else
    echo ""
    echo "⚠️ レベル2不合格 or API制限"
    echo "→ レベル3へエスカレーション"
    echo ""
    sleep 5
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# レベル3：精密検査（Pro）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "【レベル3：精密検査】Pro 💵💵💵"
echo "検査項目: 全13項目"
echo ""

PROMPT_L3="全13項目の厳格検査を実行してください：
【必須5】500行, 80文字, XSS, 機密情報, 構文エラー
【重要4】セマンティックHTML, グローバル変数, コード重複, a11y
【推奨4】コメント, 命名規則, CSSハードコード, コントラスト比

【重要】推測禁止、必ずコマンド実行結果を記録。
最終判定（Grade A-F）を下してください。"

if run_gemini_with_retry "gemini-2.5-pro" "$PROMPT_L3"; then
    echo ""
    echo "✅ レベル3（精密検査）完了"
    echo "💰 コスト: 💵💵💵💵💵💵（高）"
    echo ""
    echo "次のステップ: Claude Code最終確認を実行してください"
    exit 0
else
    echo ""
    echo "❌ レベル3でもAPI制限"
    echo ""
    echo "【対策】"
    echo "1. 翌日午前0時（太平洋時間）まで待つ"
    echo "2. Google Cloud Consoleでクォータ確認"
    echo "3. 有料プランへのアップグレード検討"
    exit 1
fi
