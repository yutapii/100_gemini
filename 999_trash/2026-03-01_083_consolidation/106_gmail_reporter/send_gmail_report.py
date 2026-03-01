#!/usr/bin/env python3
"""
send_gmail_report.py
検査レポートをGmail送信
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_report(report_file: str) -> None:
    """検査レポートをGmail送信

    Args:
        report_file: レポートファイルパス

    環境変数:
        EMAIL_USER: 送信元メールアドレス
        EMAIL_PASSWORD: Gmailアプリパスワード
        SMTP_SERVER: SMTPサーバー（デフォルト: smtp.gmail.com）
        SMTP_PORT: SMTPポート（デフォルト: 587）
    """
    # 環境変数取得
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")

    # 認証チェック
    if not email_user or not email_password:
        raise ValueError("環境変数未設定: EMAIL_USER, EMAIL_PASSWORD")

    # レポート読み込み
    if not os.path.exists(report_file):
        raise FileNotFoundError(f"レポート未発見: {report_file}")

    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()

    # メール作成
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user  # 自分宛
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    msg['Subject'] = f"[品質検査] Level 3完了 {timestamp}"
    msg.attach(MIMEText(report_content, 'plain', 'utf-8'))

    # 送信
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
        print(f"✅ Gmail送信成功: {email_user}")
    except Exception as e:
        print(f"❌ Gmail送信失敗: {e}")
        raise


def main():
    """メイン"""
    if len(sys.argv) < 2:
        print(f"使い方: {sys.argv[0]} <レポートファイル>")
        sys.exit(1)

    report_file = sys.argv[1]
    send_report(report_file)


if __name__ == "__main__":
    main()
