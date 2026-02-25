#!/bin/bash
# run_inspection.sh (v3.2 Final)
# 100_gemini Orchestrator

set -euo pipefail

TARGET_DIR="${1:-.}"
CALLER="./120_inspect_caller/120_inspect_caller.sh"
EVI_DIR="./101_evidence_collector/evidence"

echo "TARGET: $TARGET_DIR"

# EVIDENCE
rm -f "$EVI_DIR"/*.log
"./101_evidence_collector/collect_evidence.sh" "$TARGET_DIR"

W=$(ls -t "$EVI_DIR"/*_wc.log | head -1)
A=$(ls -t "$EVI_DIR"/*_awk.log | head -1)
H=$(ls -t "$EVI_DIR"/*_hardcode.log | head -1)

# AUDIT
cat << EOF | "$CALLER"
【Audit】
Target: $TARGET_DIR

【Evidence】
- wc: $(cat "$W")
- awk: $(cat "$A")
- path: $(cat "$H")

【Mission】
1. 80 chars limit.
2. No absolute paths.
3. 100 points or FAIL.
EOF
