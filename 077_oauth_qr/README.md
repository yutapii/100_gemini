# 077_oauth_qr - OAuth URL整形 + QRコード生成

iPad + Termius環境でOAuth URLをQRコードで読み取り可能にする。

## 用途

- SSH経由でClaude Codeログイン時、
  OAuth URLに改行が入る問題を解決
- iPadカメラでQRコードを読み取り、Safariで開ける

## 使い方

```bash
python 077_oauth_qr/oauth_qr.py "改行入りURL"
```

## 依存関係

```bash
pip install qrcode
```
