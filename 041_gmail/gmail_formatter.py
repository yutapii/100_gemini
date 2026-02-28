#!/usr/bin/env python3
"""
gmail_formatter.py - メッセージ構築・フォーマットモジュール

MIMEメッセージ構築、アドレスエンコード、本文取得を担当
"""

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, parseaddr

# デフォルト署名
DEFAULT_SIGNATURE = """--
―――――――――――――――――――■□■
齋藤 豊
携帯: 090-8946-3386
Gmail: yutapii@gmail.com
■□■――――――――――――――――――"""


def encode_email_address(email_address):
    """
    メールアドレスをRFC 2047形式にエンコード

    Args:
        email_address: "表示名 <email>" or "email@example.com"

    Returns:
        エンコード済みメールアドレス
    """
    name, addr = parseaddr(email_address)
    if name:
        return formataddr((name, addr))
    else:
        return addr


def add_signature(body, from_ai=None):
    """
    本文に署名を追加

    Args:
        body: 元の本文
        from_ai: 送信元AI名（署名末尾に追加）

    Returns:
        署名追加済み本文
    """
    if not body.endswith(DEFAULT_SIGNATURE):
        body = body.rstrip() + "\n\n" + DEFAULT_SIGNATURE

    if from_ai:
        body = body + f"\n\n[{from_ai} 担当AI]"

    return body


def build_message(to_email, subject, body, attachments=None, html=False,
                  cc=None):
    """
    MIMEメッセージを構築

    Args:
        to_email: 宛先
        subject: 件名
        body: 本文
        attachments: 添付ファイルパスのリスト
        html: HTML形式かどうか
        cc: CC宛先

    Returns:
        構築済みMIMEメッセージ
    """
    encoded_to = encode_email_address(to_email)
    encoded_cc = encode_email_address(cc) if cc else None
    content_type = 'html' if html else 'plain'

    if attachments:
        message = MIMEMultipart()
        message['to'] = encoded_to
        if encoded_cc:
            message['cc'] = encoded_cc
        message['subject'] = subject
        message.attach(MIMEText(body, content_type, 'utf-8'))

        for filepath in attachments:
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=('utf-8', '', filename)
                )
                message.attach(part)
                print(f"  添付: {filename}")
            else:
                print(f"  警告: ファイルなし {filepath}")
    else:
        message = MIMEText(body, content_type, 'utf-8')
        message['to'] = encoded_to
        if encoded_cc:
            message['cc'] = encoded_cc
        message['subject'] = subject

    return message


def message_to_raw(message):
    """MIMEメッセージをBase64エンコード"""
    return base64.urlsafe_b64encode(message.as_bytes()).decode()


def get_message_body(payload):
    """メッセージ本文を取得（text/plain優先）"""
    body = ''
    html_body = ''

    if 'body' in payload and payload['body'].get('data'):
        body = base64.urlsafe_b64decode(
            payload['body']['data']).decode('utf-8', errors='replace')

    if 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')
            if mime_type == 'text/plain':
                if part['body'].get('data'):
                    body = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='replace')
                    break
            elif mime_type == 'text/html':
                if part['body'].get('data'):
                    html_body = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode('utf-8', errors='replace')
            elif mime_type.startswith('multipart/'):
                nested = get_message_body(part)
                if nested:
                    body = nested
                    break

    # text/plainがなければHTMLを使用（タグ除去）
    if not body and html_body:
        body = _strip_html(html_body)

    return body


def _strip_html(html_body):
    """HTMLタグを除去してプレーンテキストを取得"""
    import re
    # style/scriptタグとその中身を除去
    body = re.sub(r'<style[^>]*>.*?</style>', '', html_body,
                  flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body,
                  flags=re.DOTALL | re.IGNORECASE)
    # headタグとその中身を除去
    body = re.sub(r'<head[^>]*>.*?</head>', '', body,
                  flags=re.DOTALL | re.IGNORECASE)
    # 残りのタグを除去
    body = re.sub(r'<[^>]+>', '', body)
    # HTMLエンティティを変換
    body = body.replace('&nbsp;', ' ').replace('&amp;', '&')
    body = body.replace('&lt;', '<').replace('&gt;', '>')
    body = body.replace('&quot;', '"')
    # 連続空行を整理
    body = re.sub(r'\n\s*\n', '\n\n', body)
    return body.strip()
