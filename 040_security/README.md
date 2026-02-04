# 040_security/ - セキュリティ設定

## 用途

このフォルダには以下のセキュリティ関連ファイルを保管：

- API キー
- 認証トークン
- パスワード（暗号化推奨）
- 秘密鍵
- その他機密情報

## .gitignore設定

**重要**: このフォルダの内容は**Gitに含めない**

`.gitignore`ファイルで除外設定済み：
```
040_security/*
!040_security/README.md
!040_security/.gitignore
```

## ファイル管理

### 命名規則
```
[サービス名]_[用途].[拡張子]
```

例：
- `gemini_api_key.txt` - Gemini API Key
- `youtube_api_token.json` - YouTube API認証情報

### 暗号化推奨

機密性の高い情報は暗号化して保存：
```bash
# 暗号化
gpg -c secret_file.txt

# 復号化
gpg secret_file.txt.gpg
```

## 環境変数

可能な限り環境変数として管理：
```bash
export GEMINI_API_KEY="your_api_key_here"
```

`.env`ファイルを使う場合：
```bash
# .env
GEMINI_API_KEY=your_api_key
YOUTUBE_API_KEY=your_key
```

**注意**: `.env`も`.gitignore`に追加すること

## アクセス権限

```bash
# このフォルダのアクセス権を制限
chmod 700 040_security/
chmod 600 040_security/*
```

## バックアップ

機密情報は別途安全な場所にバックアップ：
- 暗号化したUSBメモリ
- パスワード管理ツール（1Password, Bitwarden等）
- クラウドストレージ（暗号化必須）

---

**セキュリティは最優先。機密情報の管理には細心の注意を。**
