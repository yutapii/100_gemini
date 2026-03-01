#!/bin/bash
# night_mode_controller.sh
# 深夜帯制御（01:00-05:59判定）

set -euo pipefail

# 深夜帯判定
is_night_mode() {
    local hour=$(date +%H)
    if [ "$hour" -ge 1 ] && [ "$hour" -lt 6 ]; then
        return 0  # 深夜帯
    else
        return 1  # 日中
    fi
}

# 深夜帯待機
wait_for_night_mode() {
    local hour=$(date +%H)

    echo ""
    echo "🌙 深夜帯自動実行モード"
    echo "現在時刻: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "実行可能時間: 01:00-05:59"
    echo ""

    if is_night_mode; then
        echo "✅ 深夜帯です。実行可能です。"
        return 0
    else
        echo "⏰ 深夜帯ではありません。"

        # 次の01:00まで待機時間計算
        local wait_hours
        if [ "$hour" -ge 6 ]; then
            # 6時以降なら翌日の1時まで
            wait_hours=$((24 - hour + 1))
        else
            # 0時台なら1時まで
            wait_hours=$((1 - hour))
        fi

        echo "次回実行: 約${wait_hours}時間後"
        return 1
    fi
}

# テストモード
if [[ "${1:-}" == "--test" ]]; then
    echo "深夜帯判定テスト"
    if is_night_mode; then
        echo "✅ 現在は深夜帯（01:00-05:59）"
        exit 0
    else
        echo "❌ 現在は日中"
        exit 1
    fi
fi

# 通常モード
wait_for_night_mode
