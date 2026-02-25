import os
from pathlib import Path
from typing import Tuple, List

class WhitetoolCore:
    """
    Whitetool統治機構の中核（官邸）
    プロジェクト全体の規律、パス、品質を一元管理する。
    """
    
    def __init__(self):
        # 自身の位置からプロジェクトルートを特定
        self.root = Path(__file__).resolve().parent.parent
        self.allowed_subdirs = [
            "000_concept", "010_ai", "020_work_reports",
            "030_config", "040_security", "050_server",
            "066_evidence", "080_tps", "100_inspection_tools",
            "101_evidence_collector", "107_orchestrator",
            "120_inspect_caller", "cc_reports"
        ]

    def get_safe_path(self, rel_path: str) -> Path:
        """指定された相対パスを安全な絶対パスとして解決する"""
        target = (self.root / rel_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise PermissionError(f"Gave access denied: {rel_path}")
        return target

    def validate_code_standards(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        与党としての「規律検査」。
        単なるエラー出力ではなく、具体的な「修正の導き」を返す。
        """
        errors = []
        path = self.get_safe_path(file_path)
        
        if not path.exists():
            return False, ["File not found."]

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 1. 500行ルール
        if len(lines) > 500:
            errors.append(f"Line count ({len(lines)}) exceeds 500. Split it.")

        # 2. 80文字ルール
        for i, line in enumerate(lines, 1):
            if len(line.encode("utf-8")) > 80:
                errors.append(f"L{i}: Line length ({len(line)}) exceeds 80.")

        return len(errors) == 0, errors

    def get_system_map(self):
        """所番地（ディレクトリ構成）の妥当性をチェックする"""
        # 今後、ディレクトリ番号の重複や欠番を監視するロジックを追加予定
        pass

# グローバルな官邸インスタンス
Cabinet = WhitetoolCore()
