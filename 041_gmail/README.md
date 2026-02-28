# 041_gmail - Gmail操作（全AI共通）

**認証**: WT標準 040_security/ の認証情報を使用

---

## コマンド一覧

```bash
# 送信
python3 ~/000_Whitetool/041_gmail/gmail.py send \
  "to@example.com" "件名" "本文"
python3 ~/000_Whitetool/041_gmail/gmail.py send \
  "to@example.com" "件名" "本文" --attach file.pdf

# 受信（最新N件）
python3 ~/000_Whitetool/041_gmail/gmail.py inbox 10
python3 ~/000_Whitetool/041_gmail/gmail.py inbox 5 \
  --unread

# 検索
python3 ~/000_Whitetool/041_gmail/gmail.py search \
  "from:someone@example.com"
python3 ~/000_Whitetool/041_gmail/gmail.py search \
  "subject:請求書"

# 特定メール読み取り
python3 ~/000_Whitetool/041_gmail/gmail.py read MSG_ID

# 下書き作成
python3 ~/000_Whitetool/041_gmail/gmail.py draft \
  "to@example.com" "件名" "本文"
python3 ~/000_Whitetool/041_gmail/gmail.py draft \
  "to@example.com" "件名" "本文" --attach file.pdf

# 添付ファイル一覧
python3 ~/000_Whitetool/041_gmail/gmail.py \
  attach list MSG_ID

# 添付ファイルDL
python3 ~/000_Whitetool/041_gmail/gmail.py \
  attach download MSG_ID
python3 ~/000_Whitetool/041_gmail/gmail.py \
  attach download MSG_ID -o ~/Downloads
```

---

## モジュール構成

| ファイル | 役割 |
|----------|------|
| gmail.py | CLI（メイン） |
| gmail_auth.py | OAuth2認証 |
| gmail_sender.py | 送信・下書き |
| gmail_reader.py | 受信・検索・読取 |
| gmail_formatter.py | MIME構築・署名 |
| gmail_attachment.py | 添付DL |

---

*管理元: Whitetool / 更新日: 2026-02-28*
