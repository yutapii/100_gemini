#!/usr/bin/env python3
"""Gemini Vision API で画像を検査"""
import sys
import os
import argparse
from pathlib import Path
import google.generativeai as genai

# API キー読み込み（100_gemini用パス）
API_KEYS_PATH = (
    Path.home() / "100_gemini/040_security/api_keys.sh"
)

# セキュリティ: 画像は特定ディレクトリのみ許可
ALLOWED_IMAGE_DIR = Path.home() / "100_gemini/input"
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key and API_KEYS_PATH.exists():
    with open(API_KEYS_PATH, "r") as f:
        for line in f:
            if line.startswith("export GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

if not api_key:
    print("❌ GEMINI_API_KEY が見つかりません")
    sys.exit(1)

genai.configure(api_key=api_key)


def validate_image_path(path):
    """画像パスのバリデーション（パストラバーサル対策）"""
    img_path = Path(path).resolve()
    if not img_path.exists():
        raise FileNotFoundError(
            f"画像が見つかりません: {path}"
        )
    if not img_path.is_relative_to(ALLOWED_IMAGE_DIR):
        raise ValueError(
            f"画像パスが許可されたディレクトリ外: {path}"
        )
    return img_path


# 引数解析
parser = argparse.ArgumentParser(
    description="Gemini Vision API で画像を検査"
)
parser.add_argument("image_path", help="検査する画像ファイル")
parser.add_argument("prompt", help="検査プロンプト")
args = parser.parse_args()

image_path = validate_image_path(args.image_path)
prompt = args.prompt

# モデル選択（vendor_management.py と同じ方式）
try:
    models = genai.list_models()
    available_models = [
        m.name for m in models
        if 'generateContent' in m.supported_generation_methods
    ]
    # Vision対応モデルを優先（flash > pro-vision > pro）
    vision_models = [m for m in available_models if 'vision' in m.lower()]
    flash_models = [m for m in available_models if 'flash' in m.lower()]

    if flash_models:
        model_name = flash_models[0].replace('models/', '')
    elif vision_models:
        model_name = vision_models[0].replace('models/', '')
    else:
        model_name = available_models[0].replace('models/', '')

    model = genai.GenerativeModel(model_name)
    print(f"✅ 使用モデル: {model_name}")
except Exception as e:
    # フォールバック
    print(f"⚠️ モデル取得失敗、フォールバック: {e}")
    model = genai.GenerativeModel("gemini-pro")

# 画像アップロード
try:
    sample_file = genai.upload_file(
        path=str(image_path),
        display_name=image_path.name
    )
    print(f"✅ 画像アップロード完了: {image_path.name}")
except Exception as e:
    print(f"❌ 画像アップロード失敗: {e}")
    sys.exit(1)

# 検査実行
try:
    response = model.generate_content([sample_file, prompt])
    print(f"\n--- Gemini検査結果 ---")
    print(response.text)
    print(f"--- 検査完了 ---")
except Exception as e:
    print(f"❌ Gemini検査失敗: {e}")
    sys.exit(1)
