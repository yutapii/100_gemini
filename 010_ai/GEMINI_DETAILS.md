# Gemini 詳細マニュアル

**管理元**: CLAUDE.md からの外部参照
**更新日**: 2026-02-19

---

## Claude Codeとの連携プロトコル

### 呼び出しシナリオ

```
Claude Code: 「このコードの検査をお願い」
    ↓
Gemini CLI: コード解析→脆弱性レポート
    ↓
Claude Code: レポート受取→修正実施
```

### 連携手順

1. Claude Codeがファイルパスまたはコードを渡す
2. Gemini CLIが解析・検索を実行
3. 結果をマークダウン形式で返却
4. Claude Codeが結果を元に修正・実装

---

## 主要機能

### 1. コード点検

```bash
gemini "以下のファイルのセキュリティ診断を
実施してください：/path/to/file.js"
```

**実施内容**:
- XSS脆弱性チェック
- SQL Injection チェック
- 認証・認可の不備確認
- 情報漏洩リスク確認
- OWASP Top 10準拠チェック

### 2. Web検索

```bash
gemini "最新のReact 19の新機能について
調査してください"
```

**実施内容**:
- 公式ドキュメント検索
- 技術記事収集
- Stack Overflow検索
- GitHub Issues/PR検索

### 3. YouTube検索

```bash
gemini "Pythonの非同期処理について、
わかりやすい解説動画を探してください"
```

**実施内容**:
- キーワード検索
- 再生回数・評価でフィルタ
- 日本語/英語の言語別検索
- チャンネル信頼性確認

### 4. ファイル検査

```bash
gemini "このプロジェクト内の全JSファイルで
console.log が残っていないか確認してください"
```

**実施内容**:
- パターンマッチング
- 大量ファイルの一括処理
- レポート生成

---

## 参考資料

- WT標準ルール:
  @~/010_STP_APIv1/000_concept/WT_STANDARD_RULE.md
- STP管理パネル: http://localhost:5030/
- システム導入ガイド:
  @~/010_STP_APIv1/000_concept/NEW_SYSTEM_CHECKIN_GUIDE.md

---

*Gemini 2026-02-19*
