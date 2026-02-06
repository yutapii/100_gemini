#!/usr/bin/env python3
"""
レイヤ分け対応版：X線レイヤと文字レイヤを分離
"""

import sys
import argparse
import subprocess
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from pypdf import PdfReader, PdfWriter
from io import BytesIO


# セキュリティ: PDFは特定ディレクトリのみ許可
ALLOWED_PDF_DIRS = [
    Path.home() / "040_VitalRemind",
    Path.home() / "100_gemini/input",
    Path("/tmp"),
]


def validate_pdf_path(path, mode="read"):
    """PDFパスのバリデーション（パストラバーサル対策）"""
    pdf_path = Path(path).resolve()

    # 許可されたディレクトリ内にあるか確認
    is_allowed = any(
        pdf_path.is_relative_to(allowed_dir)
        for allowed_dir in ALLOWED_PDF_DIRS
    )
    if not is_allowed:
        raise ValueError(
            f"PDFパスが許可されたディレクトリ外: {path}"
        )

    # 読み込みモードの場合は存在確認
    if mode == "read" and not pdf_path.exists():
        raise FileNotFoundError(
            f"PDFファイルが見つかりません: {path}"
        )

    return pdf_path


def create_x_layer():
    """
    X線レイヤ：対角線を描画（座標確認用）
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setStrokeColorRGB(1, 0, 0)  # 赤色
    c.setLineWidth(0.5)

    # 記号欄（4マス）にX
    kigou_x_start = 122.6
    kigou_y_bottom = 611.3
    kigou_width = 71.3
    kigou_height = 25.4
    kigou_cell_width = kigou_width / 4

    for i in range(4):
        x_left = kigou_x_start + (kigou_cell_width * i)
        x_right = x_left + kigou_cell_width
        y_top = kigou_y_bottom + kigou_height

        # X描画
        c.line(x_left, kigou_y_bottom, x_right, y_top)
        c.line(x_left, y_top, x_right, kigou_y_bottom)

    # 番号欄（7マス）にX
    bangou_x_start = 211.4
    bangou_y_bottom = 611.6
    bangou_width = 121.5
    bangou_height = 24.2
    bangou_cell_width = bangou_width / 7

    for i in range(7):
        x_left = bangou_x_start + (bangou_cell_width * i)
        x_right = x_left + bangou_cell_width
        y_top = bangou_y_bottom + bangou_height

        # X描画
        c.line(x_left, bangou_y_bottom, x_right, y_top)
        c.line(x_left, y_top, x_right, bangou_y_bottom)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def create_text_layer(kigou="201", bangou="244306"):
    """
    文字レイヤ：記号・番号を描画

    Args:
        kigou: 記号（例："201"）
        bangou: 番号（例："244306"）
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    c.setFont('HeiseiKakuGo-W5', 11)

    # 記号（4マス）- 番号欄と同じ方式（中央配置）
    kigou_x_start = 122.6
    kigou_cell_width = 71.3 / 4
    kigou_y = 618.0

    for i, char in enumerate(kigou):
        if i < 4 and char.strip():  # 4マスまで、空白以外
            x_center = (
                kigou_x_start + (kigou_cell_width * i) +
                (kigou_cell_width / 2)
            )
            c.drawCentredString(x_center, kigou_y, char)

    # 番号（7マス）
    bangou_x_start = 211.4
    bangou_cell_width = 121.5 / 7
    bangou_y = 620.7

    for i, char in enumerate(bangou):
        if i < 7 and char.strip():  # 7マスまで、空白以外
            x_center = (
                bangou_x_start + (bangou_cell_width * i) +
                (bangou_cell_width / 2)
            )
            c.drawCentredString(x_center, bangou_y, char)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def fill_with_layers(template_pdf, output_pdf, kigou="201",
                     bangou="244306", show_x=True):
    """
    レイヤ分けしてPDFに入力

    Args:
        template_pdf: テンプレートPDF
        output_pdf: 出力PDF
        kigou: 記号
        bangou: 番号
        show_x: Xレイヤ表示（True=座標確認, False=最終版）
    """
    try:
        reader = PdfReader(template_pdf)
        writer = PdfWriter()

        page = reader.pages[0]

        # Xレイヤ（座標確認モードのみ）
        if show_x:
            x_layer = create_x_layer()
            x_reader = PdfReader(x_layer)
            page.merge_page(x_reader.pages[0])

        # 文字レイヤ（常に表示）
        text_layer = create_text_layer(kigou, bangou)
        text_reader = PdfReader(text_layer)
        page.merge_page(text_reader.pages[0])

        writer.add_page(page)

        # 残りのページ
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

        # 出力
        with open(output_pdf, "wb") as f:
            writer.write(f)

        mode_str = "座標確認（X線あり）" if show_x else "最終版"
        print(f"✅ 作成完了: {output_pdf} ({mode_str})")

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDFレイヤ分け記入"
    )
    parser.add_argument("kigou", help="記号（4桁）")
    parser.add_argument("bangou", help="番号（7桁）")
    parser.add_argument("--template",
                        default="/tmp/comsys_shobyou_form.pdf",
                        help="テンプレートPDF")
    parser.add_argument("--output",
                        default="/tmp/sample_output.pdf",
                        help="出力PDF")
    parser.add_argument("--final", action="store_true",
                        help="最終版（X線なし）")
    parser.add_argument("--no-preview", action="store_true",
                        help="プレビュー表示なし")
    args = parser.parse_args()

    # パスバリデーション
    template = str(validate_pdf_path(args.template, mode="read"))
    output = str(validate_pdf_path(args.output, mode="write"))

    show_x = not args.final

    fill_with_layers(
        template,
        output,
        args.kigou,
        args.bangou,
        show_x
    )

    print(f"確認: open {args.output}")

    if not args.no_preview:
        subprocess.run(["open", args.output])
