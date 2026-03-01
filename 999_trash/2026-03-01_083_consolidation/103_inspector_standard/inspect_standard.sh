#!/bin/bash
# inspect_standard.sh
# Level 2 Inspection (Flash)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../100_inspection_tools/common/common.sh
source "$SCRIPT_DIR/../100_inspection_tools/common/common.sh"

REPORTS_DIR="$SCRIPT_DIR/reports"
init_reports "$REPORTS_DIR"

run_standard() {
    local target_dir="${1:-.}"
    local ts
    ts="$(date '+%Y%m%d_%H%M%S')"
    local report="$REPORTS_DIR/${ts}_standard.md"

    local wc_log
    wc_log=$(get_latest_log "_wc.log")
    
    echo "Running Standard Inspection on $target_dir"
}

if [[ "${1:-}" != "--source-only" ]]; then
    run_standard "${1:-.}"
fi
