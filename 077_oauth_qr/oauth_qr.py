#!/usr/bin/env python3
"""
OAuth URL整形 + QRコード生成ツール
iPad + Termius環境でOAuth URLをQRコードで読み取り可能にする
"""
import argparse
import subprocess
import sys
import re


def clean_url(url):
    """改行・空白を除去してクリーンなURLを生成"""
    return re.sub(r'\s+', '', url.strip())


def generate_qr(url):
    """QRコード生成（qrcodeライブラリ使用）"""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        print("\nqrcodeライブラリが必要です:")
        print("pip install qrcode")
        sys.exit(1)


def copy_to_clipboard(text):
    """クリップボードにコピー（macOS）"""
    try:
        subprocess.run(
            ['pbcopy'],
            input=text.encode('utf-8'),
            check=True
        )
        print("クリップボードにコピーしました")
    except Exception as e:
        print(f"クリップボードコピー失敗: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='OAuth URL整形 + QRコード生成'
    )
    parser.add_argument(
        'url',
        nargs='?',
        help='OAuth URL（改行入りでも可）'
    )

    args = parser.parse_args()

    if args.url:
        clean = clean_url(args.url)
        print(f"クリーンURL:\n{clean}\n")
        copy_to_clipboard(clean)
        print("\nQRコード:")
        generate_qr(clean)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
