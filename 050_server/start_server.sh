#!/bin/bash
# Gemini CLI Server 起動スクリプト

cd /Users/saitoyutaka/100_gemini/050_server
python3 main.py &
echo "Gemini CLI Server started on port 5100"
