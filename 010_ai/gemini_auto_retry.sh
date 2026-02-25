#!/bin/bash
# gemini_auto_retry.sh
# 429エラー時の自動リトライ機能

set -euo pipefail

INSPECTION_PROMPT="${1:-}"
MAX_RETRIES=3
RETRY_WAIT=30

if [ -z "$INSPECTION_PROMPT" ]; then
    echo "Usage: $0 <prompt>"
    exit 1
fi

run_with_retry() {
    local attempt=1
    while [ $attempt -le $MAX_RETRIES ]; do
        echo "Attempt $attempt/$MAX_RETRIES..."
        # 修正: 引用符で囲んでスペースや記号を保護
        if gemini -y "$INSPECTION_PROMPT"; then
            return 0
        fi
        
        echo "429 or Error detected. Waiting ${RETRY_WAIT}s..."
        sleep $RETRY_WAIT
        ((attempt++))
    done
    return 1
}

run_with_retry
