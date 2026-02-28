#!/usr/bin/env python3
"""
gmail_sender.py - メール送信・下書き作成モジュール

send_email, create_draft機能を提供。
"""

from gmail_auth import get_gmail_service
from gmail_formatter import (
    add_signature,
    build_message,
    message_to_raw
)


def send_email(to_email, subject, body, attachments=None, html=False,
               from_ai=None):
    """
    メール送信

    Args:
        to_email: 宛先
        subject: 件名
        body: 本文
        attachments: 添付ファイルパスのリスト
        html: HTML形式かどうか
        from_ai: 送信元AI名（署名末尾に追加）

    Returns:
        送信結果
    """
    service = get_gmail_service()

    # 署名を追加
    body = add_signature(body, from_ai)

    # メッセージ構築
    message = build_message(to_email, subject, body, attachments, html)
    raw = message_to_raw(message)

    result = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    print(f"送信完了: {to_email}")
    print(f"件名: {subject}")
    print(f"Message ID: {result['id']}")
    return result


def create_draft(to_email, subject, body, attachments=None, html=False,
                 cc=None):
    """
    下書き作成

    Args:
        to_email: 宛先
        subject: 件名
        body: 本文
        attachments: 添付ファイルパスのリスト
        html: HTML形式かどうか
        cc: CC宛先

    Returns:
        作成された下書き
    """
    service = get_gmail_service()

    # 署名を追加
    body = add_signature(body)

    # メッセージ構築
    message = build_message(to_email, subject, body, attachments, html, cc)
    raw = message_to_raw(message)

    draft = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw}}
    ).execute()

    print(f"下書き作成完了: {to_email}")
    if cc:
        print(f"CC: {cc}")
    print(f"件名: {subject}")
    print(f"Draft ID: {draft['id']}")
    return draft
