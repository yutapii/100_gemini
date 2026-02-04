# Gemini APIクォータ管理

## 概要

Gemini CLIで使用するGoogle AI Studio APIには、料金プランごとのクォータ制限がある。適切なモデル選択により、コストとパフォーマンスのバランスを保つ。

---

## 現在の状況

**料金プラン**: 2,900円/月（Google AI Studio）

**モデルごとのクォータ**:
- `gemini-2.5-pro`: クォータ制限あり（高精度）
- `gemini-2.5-flash`: クォータ独立（高速・推奨）
- `gemini-2.5-flash-lite`: クォータ独立（超高速）

**重要**: モデルごとのクォータは独立している。Pro が枯渇しても Flash は使用可能。

---

## 問題事例

### 2026-02-04 クォータ枯渇事件

**発生時刻**: 2026-02-04 午前

**エラー内容**:
```
TerminalQuotaError: You have exhausted your capacity on this model.
Your quota will reset after 20h24m50s.
Model: gemini-2.5-pro
```

**原因**:
- gemini-2.5-pro を連続使用
- 料金プランの上限に到達

**影響**:
- 100_gemini/index.html の点検作業が一時中断

---

## 対策

### 即時対策（実施済み）

1. **設定ファイル編集**
   ```bash
   vi ~/.gemini/settings.json
   # "name": "gemini-2.5-pro" → "name": "gemini-2.5-flash" に変更
   ```

2. **動作確認**
   ```bash
   gemini -p "テストメッセージ"
   ```

3. **点検作業の再開**
   - gemini-2.5-flash で 100_gemini/index.html 点検を完了
   - クォータエラーなし

### 恒久対策

**モデル選択戦略**:

| タスク | 推奨モデル | 理由 |
|--------|----------|------|
| コード点検 | **flash** | 高速・コスト効率良・精度十分 |
| セキュリティ診断 | **flash** | 十分な精度 |
| 複雑な推論 | **pro**（制限付き） | 高度な分析が必要な場合のみ |
| YouTube検索 | **flash** | 簡易タスク |
| ドキュメント生成 | **flash** | 速度重視 |
| バグ原因分析 | **flash → pro** | まずflashで試し、必要ならpro |

**デフォルト設定**: `gemini-2.5-flash`（推奨）

---

## モデル切り替え手順

### 方法1: 設定ファイル編集（永続化）

```bash
# バックアップ作成
cp ~/.gemini/settings.json ~/.gemini/settings.json.backup

# 編集
vi ~/.gemini/settings.json

# 変更箇所
{
  "model": {
    "name": "gemini-2.5-flash"  ← ここを変更
  },
  ...
}

# 確認
cat ~/.gemini/settings.json | grep "name"
```

### 方法2: 対話式コマンド（推奨）

```bash
# Gemini CLIセッション内で実行
gemini

# セッション内で
/model

# 画面で選択
# 1. Auto (Gemini 2.5)
# 2. Manual (gemini-2.5-pro) ← ここで gemini-2.5-flash を選択

# Tab キーで「Remember for future sessions」を true に設定
# Enter で確定
```

### 方法3: コマンドラインフラグ（一時的）

```bash
# 単発実行（永続化されない）
gemini -p "プロンプト" --model gemini-2.5-flash
```

### 方法4: STPパネルスイッチ（予定）

**実装予定**: Phase 6
- STPパネル（http://localhost:5030/）にGUIスイッチ追加
- ワンクリックでモデル切り替え可能

---

## クォータリセット

**リセットタイミング**: クォータ枯渇から約20時間後

**確認方法**:
```bash
gemini -p "テスト：1+1は？"
```

エラーが出なければリセット完了。

---

## クォータ監視（将来的な改善案）

### 理想的な運用

1. **クォータ使用量の定期チェック**
   - Google AI Studio ダッシュボードで確認
   - 残量が30%以下になったらFlashに切り替え

2. **残量警告の実装**
   - STPパネルに残量表示（API提供があれば）
   - 閾値を超えたら自動通知

3. **使用量のログ記録**
   - 060_data/ にクォータ使用ログを記録
   - モデルごとの利用傾向を分析

---

## 教訓

### ✅ 良かった点

- モデルごとのクォータが独立していることを活用
- Flashモデルでも十分な品質の診断結果を取得
- 設定ファイル編集で迅速に対応

### ⚠️ 改善点

- Pro の使いすぎに注意
- 通常作業は Flash をデフォルトにすべき
- クォータ残量の可視化が必要

---

## 参考資料

**Gemini CLI設定ファイル**:
- `~/.gemini/settings.json` - モデル設定、認証情報
- `~/.gemini/.env` - API キー

**STP関連**:
- `100_gemini/030_config/gemini_cli_config.md` - Gemini CLI運用設定
- `010_STP_APIv1/110_panel/` - STPパネル（モデル切り替えスイッチ予定）

**TPS活動**:
- 080_tps/ - 継続的改善活動の記録
- 問題発生 → 分析 → 対策 → 横展開 → 品質向上

---

**作成日**: 2026-02-04
**管理**: STP🔧
**次回レビュー**: クォータリセット後（約20時間後）
