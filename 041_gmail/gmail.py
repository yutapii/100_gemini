#!/usr/bin/env python3
"""
041_gmail - 全AI共通 Gmail操作ツール

使用方法:
    # 送信
    python3 gmail.py send "to@example.com" "件名" "本文"
    python3 gmail.py send "to@example.com" "件名" "本文" --from "WFF"
    python3 gmail.py send "to@example.com" "件名" "本文" --attach file.pdf

    # 受信（最新N件）
    python3 gmail.py inbox 10
    python3 gmail.py inbox 5 --unread

    # 検索
    python3 gmail.py search "from:someone@example.com"
    python3 gmail.py search "subject:請求書"
    python3 gmail.py search "after:2025/01/01 before:2025/01/31"

    # 特定メール読み取り
    python3 gmail.py read MESSAGE_ID

    # 下書き作成
    python3 gmail.py draft "to@example.com" "件名" "本文"
    python3 gmail.py draft "to@example.com" "件名" "本文" --attach file.pdf

    # 添付ファイル操作
    python3 gmail.py attach list MSG_ID
    python3 gmail.py attach download MSG_ID
    python3 gmail.py attach download MSG_ID -o ~/Downloads

認証: 環境変数 or WT標準 040_security/

モジュール構成:
    - gmail_auth.py: 認証管理
    - gmail_formatter.py: メッセージ構築
    - gmail_sender.py: 送信・下書き
    - gmail_reader.py: 受信・検索・読取
    - gmail_attachment.py: 添付ファイルDL
    - gmail.py: メイン・CLI（このファイル）
"""

import argparse

from gmail_sender import send_email, create_draft
from gmail_reader import (
    list_inbox, search_emails, read_email,
)
from gmail_attachment import (
    list_attachments, download_all,
)


def main():
    parser = argparse.ArgumentParser(
        description='Gmail操作ツール（全AI共通）'
    )
    subparsers = parser.add_subparsers(dest='command', help='コマンド')

    # send
    send_parser = subparsers.add_parser('send', help='メール送信')
    send_parser.add_argument('to', help='宛先')
    send_parser.add_argument('subject', help='件名')
    send_parser.add_argument('body', help='本文')
    send_parser.add_argument(
        '--attach', nargs='+', help='添付ファイル')
    send_parser.add_argument(
        '--html', action='store_true', help='HTML形式')
    send_parser.add_argument(
        '--from', dest='from_ai', help='送信元AI名（例: WFF）')

    # inbox
    inbox_parser = subparsers.add_parser('inbox', help='受信トレイ表示')
    inbox_parser.add_argument(
        'count', type=int, nargs='?', default=10, help='取得件数')
    inbox_parser.add_argument(
        '--unread', action='store_true', help='未読のみ')

    # search
    search_parser = subparsers.add_parser('search', help='メール検索')
    search_parser.add_argument('query', help='検索クエリ')
    search_parser.add_argument(
        '--max', type=int, default=50, help='最大取得件数')

    # read
    read_parser = subparsers.add_parser('read', help='メール読み取り')
    read_parser.add_argument('message_id', help='メッセージID')

    # draft
    draft_p = subparsers.add_parser(
        'draft', help='下書き作成'
    )
    draft_p.add_argument('to', help='宛先')
    draft_p.add_argument('subject', help='件名')
    draft_p.add_argument('body', help='本文')
    draft_p.add_argument('--cc', help='CC宛先')
    draft_p.add_argument(
        '--attach', nargs='+', help='添付ファイル'
    )
    draft_p.add_argument(
        '--html', action='store_true',
        help='HTML形式',
    )

    # attach
    att_p = subparsers.add_parser(
        'attach', help='添付ファイル操作'
    )
    att_sub = att_p.add_subparsers(
        dest='attach_cmd', help='サブコマンド'
    )
    # attach list
    att_list = att_sub.add_parser(
        'list', help='添付一覧'
    )
    att_list.add_argument(
        'message_id', help='メッセージID'
    )
    # attach download
    att_dl = att_sub.add_parser(
        'download', help='添付DL'
    )
    att_dl.add_argument(
        'message_id', help='メッセージID'
    )
    att_dl.add_argument(
        '-o', '--output-dir', default='.',
        help='出力先（default: .）',
    )

    args = parser.parse_args()

    if args.command == 'send':
        send_email(
            args.to, args.subject, args.body,
            attachments=args.attach,
            html=args.html,
            from_ai=args.from_ai
        )
    elif args.command == 'inbox':
        list_inbox(args.count, args.unread)
    elif args.command == 'search':
        search_emails(args.query, args.max)
    elif args.command == 'read':
        read_email(args.message_id)
    elif args.command == 'draft':
        create_draft(
            args.to, args.subject, args.body,
            attachments=args.attach,
            html=args.html,
            cc=args.cc,
        )
    elif args.command == 'attach':
        if args.attach_cmd == 'list':
            list_attachments(args.message_id)
        elif args.attach_cmd == 'download':
            download_all(
                args.message_id,
                args.output_dir,
            )
        else:
            att_p.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
