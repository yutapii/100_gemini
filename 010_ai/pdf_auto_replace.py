#!/usr/bin/env python3
"""
【ミッション：傷病手当申請書の11月分を12月・1月分へ完全置換せよ】
白塗り+上書き実行
"""

import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
import argparse
import subprocess
from pathlib import Path


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


def get_date_coordinates(pdf_path):
    """pdfplumberで日付の座標を取得"""
    coords = {}

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[1]  # 2ページ目

        chars = page.chars

        # 「から」の行（y=600-625）の数字「071102」
        from_chars = [
            c for c in chars if 600 <= c['y0'] <= 625 and
            c['text'].isdigit() and 305 <= c['x0'] <= 400
        ]
        from_chars.sort(key=lambda c: c['x0'])

        if len(from_chars) >= 4:
            x0 = min([c['x0'] for c in from_chars[:6]])
            y0 = min([c['y0'] for c in from_chars[:6]])
            x1 = max([c['x1'] for c in from_chars[:6]])
            y1 = max([c['y1'] for c in from_chars[:6]])
            coords["from_date"] = (x0, y0, x1, y1)

        # 「まで」の行（y=580-605）の数字「071201」
        to_chars = [
            c for c in chars if 580 <= c['y0'] <= 605 and
            c['text'].isdigit() and 300 <= c['x0'] <= 400
        ]
        to_chars.sort(key=lambda c: c['x0'])

        if len(to_chars) >= 6:
            to_chars_target = to_chars[:6]
            x0 = min([c['x0'] for c in to_chars_target])
            y0 = min([c['y0'] for c in to_chars_target])
            x1 = max([c['x1'] for c in to_chars_target])
            y1 = max([c['y1'] for c in to_chars_target])
            coords["to_date"] = (x0, y0, x1, y1)

        # 日数「30」
        days_chars = [
            c for c in chars if c['text'].isdigit() and
            488 <= c['x0'] <= 513 and 219 <= c['y0'] <= 248
        ]
        days_chars.sort(key=lambda c: c['x0'])

        if len(days_chars) >= 2:
            x0 = min([c['x0'] for c in days_chars[:2]])
            y0 = min([c['y0'] for c in days_chars[:2]])
            x1 = max([c['x1'] for c in days_chars[:2]])
            y1 = max([c['y1'] for c in days_chars[:2]])
            coords["days"] = (x0, y0, x1, y1)

    return coords


def mask_and_replace(page, bbox, new_text, fontsize=23):
    """
    白塗り+上書き

    Args:
        page: fitz.Page
        bbox: (x0, y0, x1, y1) - pdfplumber座標系（左上原点）
        new_text: 新しいテキスト
        fontsize: フォントサイズ
    """
    # 白で塗りつぶし（余裕を持って）
    margin = 5
    white_rect = fitz.Rect(
        bbox[0] - margin,
        bbox[1] - margin,
        bbox[2] + margin,
        bbox[3] + margin
    )
    page.draw_rect(white_rect, color=(1, 1, 1), fill=(1, 1, 1))

    # 新しいテキストを描画
    # y座標はbaseline（y1から少し上）
    insert_point = fitz.Point(bbox[0], bbox[3] - 4)

    # 日本語フォント使用
    rc = page.insert_font(
        fontname="japan", fontfile="/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"
    )

    page.insert_text(
        insert_point,
        new_text,
        fontsize=fontsize,
        fontname="japan",
        color=(0, 0, 0)
    )


def create_preview_image(pdf_path, page_num=1):
    """PDFのプレビュー画像を生成"""
    doc = fitz.open(pdf_path)
    page = doc[page_num]

    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    doc.close()
    return img


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="PDF日付自動置換"
    )
    parser.add_argument("input_pdf", help="入力PDFファイル")
    parser.add_argument("output_pdf", help="出力PDFファイル")
    parser.add_argument("--no-preview", action="store_true",
                        help="プレビュー表示なし")
    args = parser.parse_args()

    # パスバリデーション
    input_pdf = str(validate_pdf_path(args.input_pdf, mode="read"))
    output_pdf = str(
        validate_pdf_path(args.output_pdf, mode="write")
    )
    preview_img_path = "/tmp/preview_after.png"

    print("=" * 60)
    print("【ステップ1】座標を取得")
    print("=" * 60)

    coords = get_date_coordinates(input_pdf)

    for key, bbox in coords.items():
        print(f"\n{key}: x0={bbox[0]:.1f} y0={bbox[1]:.1f} x1={bbox[2]:.1f} y1={bbox[3]:.1f}")

    print("\n" + "=" * 60)
    print("【ステップ2】白塗り+上書き実行")
    print("=" * 60)

    # PDFを開く
    doc = fitz.open(input_pdf)
    page = doc[1]  # 2ページ目

    # 1. 「071102」→「612０2」
    if "from_date" in coords:
        print("\n1. 申請期間（から）: 071102 → 612０2")
        mask_and_replace(page, coords["from_date"], "612０2", fontsize=18)

    # 2. 「071201」→「701０1」
    if "to_date" in coords:
        print("2. 申請期間（まで）: 071201 → 701０1")
        mask_and_replace(page, coords["to_date"], "701０1", fontsize=18)

    # 3. 「30」→「31」
    if "days" in coords:
        print("3. 日数: 30 → 31")
        mask_and_replace(page, coords["days"], "31", fontsize=28)

    # 保存
    doc.save(output_pdf)
    doc.close()

    print(f"\n✅ 作成完了: {output_pdf}")

    print("\n" + "=" * 60)
    print("【ステップ3】結果確認用プレビュー生成")
    print("=" * 60)

    # プレビュー画像生成
    preview_img = create_preview_image(output_pdf, page_num=1)
    preview_img.save(preview_img_path)

    print(f"\n✅ プレビュー画像保存: {preview_img_path}")

    # 画像を開く
    if not args.no_preview:
        subprocess.run(["open", preview_img_path])

        print("\n" + "=" * 60)
        print("【完了】確認してください")
        print("=" * 60)
        print("プレビュー画像を確認してください。")
        print("問題なければ PASS と入力してください。")
    print("=" * 60)


if __name__ == "__main__":
    main()
