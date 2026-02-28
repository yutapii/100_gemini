#!/usr/bin/env python3
"""
gmail_auth.py - Gmail認証管理モジュール（汎用版）

認証情報の場所:
  環境変数 GMAIL_CREDS_DIR または WT標準 040_security/
"""

import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# スコープ（読み書き両方）
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

# 認証情報の場所（環境変数 or WT標準）
CREDS_DIR = os.environ.get(
    'GMAIL_CREDS_DIR',
    os.path.expanduser('~/000_Whitetool/040_security')
)
CREDENTIALS_FILE = os.path.join(CREDS_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(CREDS_DIR, 'token_gmail.json')


def get_gmail_service():
    """Gmail APIサービスを取得"""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"エラー: {CREDENTIALS_FILE} が見つかりません")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
