#!/bin/bash
# setup_launchd.sh
# 深夜帯自動実行のlaunchd設定スクリプト

set -euo pipefail

PLIST_NAME="com.gemini.inspection.nightly"
PLIST_SRC="$(dirname "$0")/${PLIST_NAME}.plist"
PLIST_DST="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"

echo ""
echo "🌙 Gemini品質検査 深夜帯自動実行 セットアップ"
echo "================================================"
echo ""

# 引数チェック
case "${1:-install}" in
    install)
        echo "【インストール】"

        # 既存があればアンロード
        if launchctl list | grep -q "$PLIST_NAME"; then
            echo "既存設定をアンロード..."
            launchctl unload "$PLIST_DST" 2>/dev/null || true
        fi

        # コピー
        echo "plistをコピー: $PLIST_DST"
        cp "$PLIST_SRC" "$PLIST_DST"

        # ロード
        echo "launchdにロード..."
        launchctl load "$PLIST_DST"

        # 確認
        if launchctl list | grep -q "$PLIST_NAME"; then
            echo ""
            echo "✅ セットアップ完了"
            echo ""
            echo "実行スケジュール: 毎日 02:00"
            echo "ログ出力先: ~/100_gemini/020_work_reports/nightly.log"
            echo ""
        else
            echo "❌ ロード失敗"
            exit 1
        fi
        ;;

    uninstall)
        echo "【アンインストール】"

        if launchctl list | grep -q "$PLIST_NAME"; then
            launchctl unload "$PLIST_DST"
        fi

        if [[ -f "$PLIST_DST" ]]; then
            rm "$PLIST_DST"
        fi

        echo "✅ アンインストール完了"
        ;;

    status)
        echo "【ステータス確認】"

        if launchctl list | grep -q "$PLIST_NAME"; then
            echo "✅ 登録済み（有効）"
            launchctl list | grep "$PLIST_NAME"
        else
            echo "❌ 未登録"
        fi
        ;;

    test)
        echo "【手動テスト実行】"
        echo "107_orchestrator/run_inspection.sh を実行..."
        cd "$HOME/100_gemini/107_orchestrator"
        ./run_inspection.sh "$HOME/100_gemini" --force
        ;;

    *)
        echo "使い方: $0 [install|uninstall|status|test]"
        exit 1
        ;;
esac
