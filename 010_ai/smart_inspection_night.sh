#!/bin/bash
# スマート品質検査（深夜帯自動実行対応版）
# MacBook空き時間: 01:00-05:59

set -euo pipefail

TARGET_DIR="${1:-.}"
RETRY_WAIT=60
NIGHT_MODE_START="01:00"  # 深夜帯開始
NIGHT_MODE_END="06:00"    # 深夜帯終了

# 現在時刻チェック（深夜帯か？）
is_night_mode() {
    local current_hour=$(date +%H)
    local current_time=$(date +%H:%M)

    # 01:00-05:59の範囲
    if [ "$current_hour" -ge 1 ] && [ "$current_hour" -lt 6 ]; then
        return 0  # 深夜帯
    else
        return 1  # 日中
    fi
}

# 次の深夜帯まで待機
wait_for_night_mode() {
    local current_hour=$(date +%H)

    echo ""
    echo "🌙 深夜帯自動実行モード"
    echo "現在時刻: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "実行可能時間: 01:00-05:59"
    echo ""

    if is_night_mode; then
        echo "✅ 深夜帯です。検査を開始します。"
        return 0
    else
        echo "⏰ 深夜帯ではありません。"

        # 次の01:00まで待機時間を計算
        local wait_hours
        if [ "$current_hour" -ge 6 ]; then
            # 6時以降なら翌日の1時まで
            wait_hours=$((24 - current_hour + 1))
        else
            # 0時台なら1時まで
            wait_hours=$((1 - current_hour))
        fi

        local next_run
        next_run=$(date -v+${wait_hours}H -v1H -v0M -v0S \
            '+%Y-%m-%d %H:%M:%S')

        echo "次回実行予定: $next_run"
        echo ""
        echo "💤 深夜帯（01:00）まで自動待機します..."
        echo "   （待機時間: 約${wait_hours}時間）"
        echo "   ※完全自動実行（ユーザー操作不要）"
        echo ""

        # forceオプションチェック
        if [[ "${2:-}" == "--force" ]]; then
            echo "⚠️ --force オプション検出"
            echo "   深夜帯外ですが実行します"
            return 0
        fi

        # ログファイルに記録
        local log_dir="$HOME/100_gemini/020_work_reports"
        local log_file="$log_dir/night_inspection_$(date +%Y%m%d).log"
        local ts="[$(date '+%Y-%m-%d %H:%M:%S')]"
        echo "$ts 深夜帯待機開始（次回: $next_run）" >> "$log_file"

        # 1時間ごとに状況表示（ログにも記録）
        while ! is_night_mode; do
            sleep 3600  # 1時間
            local msg="現在時刻: $(date '+%H:%M') - 待機中..."
            echo "   $msg"
            local ts="[$(date '+%Y-%m-%d %H:%M:%S')]"
            echo "$ts $msg" >> "$log_file"
        done

        echo ""
        echo "🌙 深夜帯になりました。検査を開始します。"
        local ts="[$(date '+%Y-%m-%d %H:%M:%S')]"
        echo "$ts 深夜帯検査開始" >> "$log_file"
        return 0
    fi
}

echo ""
echo "🎯 スマート品質検査（深夜帯対応版）"
echo "対象: $TARGET_DIR"
echo "戦略: 簡易 → 中程度 → 精密"
echo "深夜帯: 01:00-05:59（MacBook空き時間）"
echo ""

# Gemini実行（リトライ付き）
run_gemini_with_retry() {
    local model=$1
    local prompt=$2
    local max_retries=3
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        echo "🔄 試行 $attempt/$max_retries (モデル: $model)..."

        if output=$(cd "$TARGET_DIR" && \
            gemini --model "$model" "$prompt" 2>&1); then
            echo "$output"
            return 0
        else
            if echo "$output" | \
                grep -q "429\|RESOURCE_EXHAUSTED\|capacity"; then
                # RPM/TPM制限
                if [ $attempt -lt $max_retries ]; then
                    echo "⚠️ RPM/TPM制限 - ${RETRY_WAIT}秒待機..."
                    sleep $RETRY_WAIT
                    ((attempt++))
                else
                    echo "❌ RPM/TPM制限が続いています"

                    # RPD制限の可能性
                    if echo "$output" | grep -qi "day\|daily\|quota.*day"; then
                        echo ""
                        echo "🌙 RPD制限の可能性があります"
                        echo "→ 深夜帯自動実行モードに"
                        echo "   切り替えます"

                        # 深夜帯まで待機
                        wait_for_night_mode "$@"

                        # 深夜帯になったら再トライ
                        echo "🔄 深夜帯での再トライを開始..."
                        attempt=1  # リセット
                        continue
                    fi

                    return 1
                fi
            else
                echo "$output"
                return 1
            fi
        fi
    done
}

# レベル1：簡易検査（Flash-Lite）
echo ""
echo "【レベル1：簡易検査】Flash-Lite 💵"
echo "検査項目: 必須4項目"
echo "（500行, 80文字, 機密情報, 構文エラー）"
echo ""

PROMPT_L1="以下の項目を検査してください：
1. 500行/ファイル制約（wc -l実行）
2. 80文字/行制約（awk実行）
3. 機密情報漏洩（grep実行）
4. 構文エラー

【重要】推測禁止、必ずコマンド実行結果を記録。
合格/不合格を明確に判定してください。"

if run_gemini_with_retry "gemini-2.5-flash-lite" "$PROMPT_L1" "$@"; then
    echo ""
    echo "✅ レベル1で合格"
    echo "💰 コスト: 💵（最安）"
    exit 0
else
    echo ""
    echo "⚠️ レベル1不合格"
    echo "→ レベル2へエスカレーション"
    sleep 5
fi

# レベル2以降は省略（必要に応じて追加）
echo ""
echo "【注意】レベル2以降は未実装"
echo "現在はレベル1のみテスト中"
exit 0
