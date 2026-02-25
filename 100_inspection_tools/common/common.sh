#!/bin/bash
# common.sh
# Shared logic for inspection scripts

set -euo pipefail

# Constants
readonly BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
readonly COLLECTOR_DIR="$BASE_DIR/101_evidence_collector"
# 統一レポートディレクトリ
readonly REPORTS_BASE_DIR="$BASE_DIR/cc_reports"

# Ensure reports directory exists
init_reports() {
    mkdir -p "$REPORTS_BASE_DIR"
}

# Find latest evidence log
get_latest_log() {
    local pattern="$1"
    ls -t "$COLLECTOR_DIR/evidence"/*"$pattern" 2>/dev/null | head -1 || echo ""
}
