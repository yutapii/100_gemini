#!/usr/bin/env python3
"""
gmail_reader.py - メール受信・検索・読取モジュール

list_inbox, search_emails, read_email機能を提供。
"""

from gmail_auth import get_gmail_service
from gmail_formatter import get_message_body


def list_inbox(max_results=10, unread_only=False):
    """
    受信トレイを表示

    Args:
        max_results: 取得件数
        unread_only: 未読のみ

    Returns:
        メール情報のリスト
    """
    service = get_gmail_service()

    query = 'in:inbox'
    if unread_only:
        query += ' is:unread'

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print("メールがありません")
        return []

    print(f"{'='*70}")
    print(f"受信トレイ（{len(messages)}件）")
    print(f"{'='*70}")

    email_list = []
    for msg in messages:
        email_info = _get_message_metadata(service, msg['id'])
        email_list.append(email_info)
        _print_email_summary(email_info)

    return email_list


def search_emails(query, max_results=20):
    """
    メール検索

    Args:
        query: 検索クエリ（Gmail検索構文）
        max_results: 最大取得件数

    検索例:
        from:someone@example.com
        to:someone@example.com
        subject:請求書
        after:2025/01/01
        before:2025/01/31
        has:attachment
        is:unread

    Returns:
        メール情報のリスト
    """
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        print(f"検索結果: 0件")
        return []

    print(f"{'='*70}")
    print(f"検索: {query}")
    print(f"結果: {len(messages)}件")
    print(f"{'='*70}")

    email_list = []
    for msg in messages:
        email_info = _get_message_metadata(service, msg['id'])
        email_list.append(email_info)
        _print_email_summary(email_info, show_unread=False)

    return email_list


def read_email(message_id):
    """
    特定のメールを読み取り

    Args:
        message_id: メッセージID

    Returns:
        メール情報（本文含む）
    """
    service = get_gmail_service()

    msg = service.users().messages().get(
        userId='me',
        id=message_id,
        format='full'
    ).execute()

    headers = {h['name']: h['value']
               for h in msg['payload']['headers']}

    print(f"{'='*70}")
    print(f"From: {headers.get('From', '')}")
    print(f"To: {headers.get('To', '')}")
    print(f"Subject: {headers.get('Subject', '')}")
    print(f"Date: {headers.get('Date', '')}")
    print(f"{'='*70}")

    body = get_message_body(msg['payload'])
    print(body)
    print(f"{'='*70}")

    return {
        'id': message_id,
        'from': headers.get('From', ''),
        'to': headers.get('To', ''),
        'subject': headers.get('Subject', ''),
        'date': headers.get('Date', ''),
        'body': body
    }


def _get_message_metadata(service, msg_id):
    """メッセージのメタデータを取得"""
    msg_data = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='metadata',
        metadataHeaders=['From', 'Subject', 'Date']
    ).execute()

    headers = {h['name']: h['value']
               for h in msg_data['payload']['headers']}

    is_unread = 'UNREAD' in msg_data.get('labelIds', [])

    return {
        'id': msg_id,
        'from': headers.get('From', ''),
        'subject': headers.get('Subject', '(件名なし)'),
        'date': headers.get('Date', ''),
        'unread': is_unread
    }


def _print_email_summary(email_info, show_unread=True):
    """メール概要を表示"""
    if show_unread and email_info.get('unread'):
        unread_mark = '[未読]'
    else:
        unread_mark = ''

    print(f"{unread_mark} {email_info['subject'][:50]}")
    print(f"   From: {email_info['from'][:40]}")
    print(f"   Date: {email_info['date'][:30]}")
    print(f"   ID: {email_info['id']}")
    print()
