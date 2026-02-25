#!/bin/bash
# start_server.sh

# スクリプトの場所へ移動（ハードコード排除）
cd "$(dirname "$0")"

# サーバー起動
python3 main.py >> gemini-server.log 2>&1 &
echo "Gemini Server started on port 5100"
