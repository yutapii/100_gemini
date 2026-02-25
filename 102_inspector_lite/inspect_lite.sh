#!/bin/bash
# inspect_lite.sh
# Level 1 Inspection (Flash-Lite)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../100_inspection_tools/common/common.sh
source "$SCRIPT_DIR/../100_inspection_tools/common/common.sh"

# 共通ディレクトリを使用
init_reports

run_lite() {
    local target_dir="${1:-.}"
    local ts
    ts="$(date '+%Y%m%d_%H%M%S')"
    # REPORTS_BASE_DIR を使用するように修正
    local report="$REPORTS_BASE_DIR/${ts}_lite.md"

    local wc_log
    wc_log=$(get_latest_log "_wc.log")
    
    echo "Running Lite Inspection on $target_dir -> $report"
}

if [[ "${1:-}" != "--source-only" ]]; then
    run_lite "${1:-.}"
fi
