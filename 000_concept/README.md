# 100_Gemini - Claude Code苦手科目サポートシステム

## システム概要

**Gemini CLI**は、Claude Codeの弱点を補完する専門AIシステムです。

### 役割

Claude Codeが苦手な以下の分野を担当：
- **コード点検**: セキュリティ診断、品質チェック
- **Web検索**: 最新技術情報の収集
- **YouTube検索**: 技術解説動画の検索
- **大量ファイル検査**: パターンマッチング、一括処理

### システム情報

| 項目 | 値 |
|------|-----|
| 番地 | 100 |
| ポート | 5100 |
| 管理元 | STP (http://localhost:5030/) |
| WT標準準拠 | 000-099番地のみ |

## アーキテクチャ

```
┌─────────────────────────────────────────┐
│         STP Management Panel            │
│        (http://localhost:5030/)         │
└────────────────┬────────────────────────┘
                 │
                 ├─ 起動/停止制御
                 ├─ ステータス監視
                 └─ AI制御（geminiコマンド）
                 │
┌────────────────▼────────────────────────┐
│          100_Gemini System              │
│            Port: 5100                   │
├─────────────────────────────────────────┤
│ WT Standard (000-099):                  │
│  ├─ 000_concept/  (Design docs)         │
│  ├─ 010_ai/       (CLAUDE.md)           │
│  ├─ 050_server/   (Server startup)      │
│  └─ 999_trash/    (Archive)             │
│                                         │
│ Custom Area (100+):                     │
│  └─ (Gemini-specific tools)             │
└─────────────────────────────────────────┘
                 │
                 ├─ Code inspection
                 ├─ Web search
                 └─ YouTube search
                 │
┌────────────────▼────────────────────────┐
│           Claude Code                   │
│    (Calls Gemini for assistance)       │
└─────────────────────────────────────────┘
```

## Claude Codeとの連携

### ワークフロー

```
1. Claude Code: コード実装完了
   ↓
2. Gemini CLI: セキュリティ診断実施
   ↓
3. Claude Code: 診断結果を受け取り、脆弱性修正
   ↓
4. Gemini CLI: 再診断・合格判定
   ↓
5. 完了
```

### 呼び出し方法

**Claude Codeから**:
```bash
# ターミナルでGemini CLIを呼び出す
gemini "このファイルのセキュリティ診断をお願いします: path/to/file.js"
```

**STPパネルから**:
- AI ONスイッチをONにする
- 自動的にターミナルが開き、Gemini CLIが起動

## フォルダ構成

### WT標準（000-099）

| フォルダ | 用途 | 必須 |
|---------|------|------|
| 000_concept/ | 設計ドキュメント | ✅ |
| 010_ai/ | AI設定（CLAUDE.md） | ✅ |
| 020_work_reports/ | 作業報告 | ✅ |
| 021_pending/ | タスク管理 | ✅ |
| 030_config/ | 設定ファイル | ✅ |
| 040_security/ | セキュリティ | ○ |
| 050_server/ | サーバー起動 | ✅ |
| 060_data/ | データ保存 | ○ |
| 080_tps/ | 改善活動 | ○ |
| 999_trash/ | アーカイブ | ✅ |

### 独自領域（100+）

100番以降は自由に設計可能。
例：
- `100_inspection_tools/` - 検査ツール
- `110_search_scripts/` - 検索スクリプト
- `120_youtube_cache/` - YouTube検索キャッシュ

## WT標準準拠

**必読**: `/Users/saitoyutaka/010_STP_APIv1/000_concept/WT_STANDARD_RULE.md`

### 絶対ルール

```
❌ 050_server/を削除・移動・リネーム禁止
❌ 000-099番地のフォルダを移動禁止
✅ 100番以降は自由設計
```

## 起動方法

### 手動起動
```bash
cd ~/100_gemini
gemini "起動の作法を実行してください"
```

### STPパネルから起動
1. http://localhost:5030/ を開く
2. Geminiカードの「AI ON」スイッチをONにする
3. ターミナルが自動的に開く

## サーバー情報

- **起動スクリプト**: `050_server/main.py`
- **ポート**: 5100
- **ヘルスチェック**: `curl http://localhost:5100/api/health`
- **停止**: `curl -X POST -H "X-STP-Request: true" http://localhost:5100/api/shutdown`

## 開発履歴

- **2026-02-04**: システム統合完了、STPパネル追加
- **2026-02-04**: WT標準フォルダ構成完成

## 関連ドキュメント

- **AI設定**: `010_ai/CLAUDE.md`
- **WT標準**: `/Users/saitoyutaka/010_STP_APIv1/000_concept/WT_STANDARD_RULE.md`
- **STP導入ガイド**: `/Users/saitoyutaka/010_STP_APIv1/000_concept/NEW_SYSTEM_CHECKIN_GUIDE.md`
