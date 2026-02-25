import sys
import os
from pdf_utils import validate_pdf_path

def fill_pdf_layers(pdf_path, layer_data):
    """PDFのレイヤーにデータを流し込む（モック実装）"""
    # 共通バリデーション（pdf_utilsへ委譲済み）
    success, msg = validate_pdf_path(pdf_path)
    if not success:
        print(f"Error: {msg}")
        return False
    
    print(f"Filling layers in {pdf_path} with {layer_data}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pdf_fill_layers.py <path> <json_data>")
        sys.exit(1)
    fill_pdf_layers(sys.argv[1], sys.argv[2])
