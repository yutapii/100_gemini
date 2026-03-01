#!/bin/bash
# inspect_pro.sh
# 100_gemini Pro Audit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=../100_inspection_tools/common/common.sh
source "$SCRIPT_DIR/../100_inspection_tools/common/common.sh"

run_pro() {
    local target="${1:-.}"
    local caller="$BASE_DIR/120_inspect_caller/120_inspect_caller.sh"
    
    # Audit using shared caller
    echo "Audit: $target"
    "$BASE_DIR/107_orchestrator/run_inspection.sh" "$target"
}

if [[ "${1:-}" != "--source-only" ]]; then
    run_pro "${1:-.}"
fi
