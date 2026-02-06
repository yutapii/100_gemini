#!/bin/bash
# run_inspection.sh
# 統合制御（3段階エスカレーション）

set -euo pipefail

# 定数
readonly BASE_DIR="$HOME/100_gemini"
readonly COLLECTOR="$BASE_DIR/101_evidence_collector"
readonly LITE="$BASE_DIR/102_inspector_lite"
readonly STANDARD="$BASE_DIR/103_inspector_standard"
readonly PRO="$BASE_DIR/104_inspector_pro"
readonly NIGHT="$BASE_DIR/105_night_mode"
readonly GMAIL="$BASE_DIR/106_gmail_reporter"

# 引数
readonly TARGET_DIR="${1:-.}"
readonly FORCE="${2:-}"

# ヘルプ
if [[ "$TARGET_DIR" == "--help" ]]; then
    echo "使い方: $0 <対象ディレクトリ> [--force]"
    echo ""
    echo "オプション:"
    echo "  --force : 深夜帯チェックをスキップ"
    exit 0
fi

# Geminiリトライ実行
run_with_retry() {
    local cmd="$1"
    local max_retries=3
    local retry_wait=60
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        echo "🔄 試行 $attempt/$max_retries..."

        if eval "$cmd"; then
            return 0
        else
            if [ $attempt -lt $max_retries ]; then
                echo "⚠️ リトライ待機（${retry_wait}秒）..."
                sleep $retry_wait
                ((attempt++))
            else
                return 1
            fi
        fi
    done
}

# メイン
main() {
    echo ""
    echo "🎯 品質検査統合制御"
    echo "対象: $TARGET_DIR"
    echo ""

    # STEP 1: 証跡収集
    echo "【STEP 1】証跡収集"
    if ! "$COLLECTOR/collect_evidence.sh" "$TARGET_DIR"; then
        echo "❌ 証跡収集失敗"
        exit 1
    fi

    # 最新証跡ディレクトリ取得
    local evidence_dir="$COLLECTOR/evidence"

    # STEP 2: 簡易検査（Level 1）
    echo ""
    echo "【STEP 2】簡易検査（Flash-Lite 💵）"
    if run_with_retry \
        "$LITE/inspect_lite.sh '$evidence_dir' '$TARGET_DIR'"; then
        echo "✅ 簡易検査合格"
        exit 0
    fi

    # STEP 3: 標準検査（Level 2）
    echo ""
    echo "【STEP 3】標準検査（Flash 💵💵💵）"
    if run_with_retry \
        "$STANDARD/inspect_standard.sh '$evidence_dir' '$TARGET_DIR'"; then
        echo "✅ 標準検査合格"
        exit 0
    fi

    # STEP 4: 精密検査（Level 3、深夜帯のみ）
    echo ""
    echo "【STEP 4】精密検査（Pro 💵💵💵💵💵💵）"

    # 深夜帯チェック（--forceでスキップ）
    if [[ "$FORCE" != "--force" ]]; then
        if ! "$NIGHT/night_mode_controller.sh" --test; then
            echo "⚠️ 深夜帯のみ実行可能（01:00-05:59）"
            echo "または --force オプションで強制実行"
            exit 1
        fi
    fi

    if run_with_retry \
        "$PRO/inspect_pro.sh '$evidence_dir' '$TARGET_DIR'"; then
        echo "✅ 精密検査合格"

        # Gmail送信
        local latest_report=$(ls -t "$PRO/reports/"*.md | head -1)
        if [[ -n "$latest_report" ]]; then
            echo ""
            echo "📧 Gmail送信中..."
            if python3 "$GMAIL/send_gmail_report.py" \
                "$latest_report"; then
                echo "✅ Gmail送信成功"
            else
                echo "⚠️ Gmail送信失敗（検査は合格）"
            fi
        fi

        exit 0
    fi

    echo "❌ 全検査不合格"
    exit 1
}

# 実行
main
