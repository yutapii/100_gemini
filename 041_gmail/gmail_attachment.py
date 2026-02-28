#!/usr/bin/env python3
"""
gmail_attachment.py - Gmail添付ファイル操作モジュール

041_gmail統合版。047_gmail_attachmentから移植・改善。
認証は gmail_auth.py に委譲。

改善点:
  - inline画像除外（署名ロゴ等をスキップ）
  - パストラバーサル防止
  - ファイル名重複時の連番付与
  - 大容量ファイル警告（20MB超）
  - 部分失敗レポート
"""

import base64
from pathlib import Path

from gmail_auth import get_gmail_service


def _safe_filepath(output_dir, filename):
    """安全なファイルパスを生成"""
    safe_name = Path(filename).name
    if not safe_name:
        safe_name = 'unnamed_attachment'
    dest = Path(output_dir) / safe_name
    if dest.exists():
        stem = dest.stem
        suffix = dest.suffix
        counter = 1
        while dest.exists():
            dest = (
                Path(output_dir)
                / f"{stem}_{counter}{suffix}"
            )
            counter += 1
    return dest


def get_attachments(service, message_id):
    """添付ファイル情報を取得（inline除外）"""
    msg = service.users().messages().get(
        userId='me', id=message_id
    ).execute()
    attachments = []

    def _find(parts):
        for part in parts:
            filename = part.get('filename', '')
            if not filename:
                if 'parts' in part:
                    _find(part['parts'])
                continue
            headers = {
                h['name']: h['value']
                for h in part.get('headers', [])
            }
            disp = headers.get(
                'Content-Disposition', ''
            )
            if 'inline' in disp:
                continue
            att_id = (
                part.get('body', {}).get('attachmentId')
            )
            size = part.get('body', {}).get('size', 0)
            attachments.append({
                'filename': filename,
                'attachment_id': att_id,
                'size': size,
                'mime_type': part.get('mimeType', ''),
            })
            if 'parts' in part:
                _find(part['parts'])

    payload = msg.get('payload', {})
    if 'parts' in payload:
        _find(payload['parts'])
    return attachments


def download_attachment(
    service, message_id, attachment_id,
    filename, output_dir
):
    """1ファイルDL（安全版）"""
    att = service.users().messages().attachments().get(
        userId='me', messageId=message_id,
        id=attachment_id
    ).execute()
    data = base64.urlsafe_b64decode(att['data'])
    dest = _safe_filepath(output_dir, filename)
    dest.write_bytes(data)
    return str(dest)


def list_attachments(message_id):
    """添付ファイル一覧を表示"""
    service = get_gmail_service()
    atts = get_attachments(service, message_id)
    if not atts:
        print("添付ファイルなし")
        return
    n = len(atts)
    print(f"=== 添付ファイル一覧（{n}件）===")
    for i, a in enumerate(atts, 1):
        kb = a['size'] / 1024
        print(f"{i}. {a['filename']}")
        print(f"   サイズ: {kb:.1f} KB")
        print(f"   MIME: {a['mime_type']}")


def download_all(message_id, output_dir='.'):
    """全添付ファイルをDL（部分失敗レポート付き）"""
    service = get_gmail_service()
    atts = get_attachments(service, message_id)
    if not atts:
        print("添付ファイルなし")
        return []
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    downloaded, failed = [], []
    for a in atts:
        if not a['attachment_id']:
            continue
        try:
            mb = a['size'] / 1024 / 1024
            if mb > 20:
                print(f"  警告: 大容量 {mb:.0f}MB")
            path = download_attachment(
                service, message_id,
                a['attachment_id'],
                a['filename'], output_dir,
            )
            print(f"  DL: {a['filename']} -> {path}")
            downloaded.append(path)
        except Exception as e:
            print(f"  失敗: {a['filename']} ({e})")
            failed.append(a['filename'])
    ok = len(downloaded)
    ng = len(failed)
    print(f"--- 結果: 成功{ok}件 / 失敗{ng}件 ---")
    return downloaded
