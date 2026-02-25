import os
from path_utils import get_safe_path

def validate_pdf_path(pdf_path):
    """PDFパスの妥当性を検証する（path_utilsへ委譲）"""
    try:
        if not pdf_path.lower().endswith(".pdf"):
            return False, "Not a PDF."
        
        # path_utilsによる厳格なホワイトリストチェック
        abs_path = get_safe_path(pdf_path)
        
        if not os.path.exists(abs_path):
            return False, "File not found."
            
        return True, "OK"
    except Exception as e:
        return False, str(e)
