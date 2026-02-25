import os
from pathlib import Path

# プロジェクトルートを動的に取得
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 安全な操作が許可されるディレクトリ（ホワイトリスト）
ALLOWED_SUBDIRS = [
    "020_work_reports", 
    "066_evidence", 
    "input", 
    "999_trash"
]

def get_safe_path(relative_path):
    """
    相対パスをPROJECT_ROOT配下の安全な絶対パスに変換。
    """
    # 物理的な改行で80文字制限遵守
    target_path = (PROJECT_ROOT / relative_path).resolve()
    
    # PROJECT_ROOT配下であることの確認
    if not str(target_path).startswith(str(PROJECT_ROOT)):
        raise PermissionError(f"Out of root: {relative_path}")
    
    # 許可されたサブディレクトリ内であることの確認
    is_allowed = any(
        str(target_path).startswith(str(PROJECT_ROOT / subdir))
        for subdir in ALLOWED_SUBDIRS
    )
    
    if not is_allowed:
        msg = f"Restricted: {relative_path}"
        raise PermissionError(msg)
        
    return target_path

def get_api_key_path():
    """APIキーファイルのパスを取得"""
    return PROJECT_ROOT / "040_security/api_keys.sh"
