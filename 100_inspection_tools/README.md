# Gemini品質検査システム

**バージョン**: v1.3
**最終更新**: 2026-02-06
**制定者**: STP専属AI

---

## 概要

AIの「やりました詐欺」を防ぐ、証跡ベース品質検査システム。

**核心設計**:
```
スクリプト自身がコマンド実行 → 証跡ファイルに記録 → AIは読むだけ
```

---

## モジュール構成

| 番号 | 名称 | 役割 |
|------|------|------|
| 100 | inspection_tools | 計画書・メインツール |
| 101 | evidence_collector | 証跡収集（wc, awk, grep） |
| 102 | inspector_lite | 簡易検査（Flash-Lite） |
| 103 | inspector_standard | 中程度検査（Flash） |
| 104 | inspector_pro | 精密検査（Pro） |
| 105 | night_mode | 深夜帯自動実行 |
| 106 | gmail_reporter | Gmail送信 |
| 107 | orchestrator | 統合制御 |
| 108 | cc_verifier | CC検証（Gemini判定の実証） |

---

## 3段階エスカレーション

```
Level 1（簡易）
    ↓ NG
Level 2（中程度）
    ↓ NG
Level 3（精密）※深夜帯のみ
```

### Level 1: 簡易検査
- **モデル**: gemini-2.5-flash-lite
- **コスト**: 💵
- **所要時間**: 2-3分
- **検査項目**: 🔴必須4項目

### Level 2: 中程度検査
- **モデル**: gemini-2.5-flash
- **コスト**: 💵💵
- **所要時間**: 5-7分
- **検査項目**: 🔴必須5 + 🟡重要4

### Level 3: 精密検査
- **モデル**: gemini-2.5-pro
- **コスト**: 💵💵💵💵💵💵
- **所要時間**: 15-20分
- **検査項目**: 🔴必須5 + 🟡重要4 + 🟢推奨4

---

## 検査項目

### 🔴 必須（不合格=即NG）
1. 500行/ファイル制約
2. 80文字/行制約
3. XSS脆弱性
4. 機密情報漏洩
5. コンソールエラー

### 🟡 重要（減点対象）
6. セマンティックHTML
7. グローバル変数多用
8. コード重複
9. アクセシビリティ

### 🟢 推奨（Grade判定）
10. コメント充実度
11. 命名規則
12. CSSハードコーディング
13. コントラスト比

---

## 使い方

### 手動実行

```bash
# 統合検査（推奨）
cd ~/100_gemini/107_orchestrator
./run_inspection.sh <対象ディレクトリ>

# 深夜帯チェックをスキップ
./run_inspection.sh <対象ディレクトリ> --force

# 個別モジュール実行
./101_evidence_collector/collect_evidence.sh <対象DIR>
./102_inspector_lite/inspect_lite.sh <証跡DIR> <対象DIR>
./108_cc_verifier/verify_gemini.sh <レポート> <証跡DIR> <対象DIR>
```

### 自動実行（深夜帯）

```bash
# launchd設定
cd ~/100_gemini/105_night_mode

# インストール
./setup_launchd.sh install

# ステータス確認
./setup_launchd.sh status

# アンインストール
./setup_launchd.sh uninstall

# 手動テスト
./setup_launchd.sh test
```

**スケジュール**: 毎日 02:00
**ログ**: ~/100_gemini/020_work_reports/nightly.log

---

## GC+CC相互監視

**GC（Gemini CLI）の役割**:
- 証跡ファイルを読んで一次分析
- 重大度判定、修正提案

**CC（Claude Code）の役割**:
- GCの分析結果を検証
- GCのハルシネーション検出
- 最終判定

**効果**:
- GCとCCは構造が違う → 同じバイアスを持たない
- 信頼性: 単独AIより高い

---

## Phase間フィードバックループ

```
Phase N実施
    ↓
証跡収集（101_evidence_collector/）
    ↓
Gemini分析（102-104_inspector_*/）
    ↓
CC検証（108_cc_verifier/）
    ↓
判定結果に基づき次Phase実施
```

**判定基準**:
1. Phase完了 + 問題なし → 次Phase実施
2. Phase完了 + 問題あり → 修正後再実施
3. Phase完了 + 次Phase不要 → 作業完了
4. Phase完了 + 判定不明 → ユーザー確認

---

## 証跡ファイル

**保存先**: ~/100_gemini/101_evidence_collector/evidence/

**命名規則**: `YYYYMMDD_HHMMSS_<項目>.log`

**保持期間**: 30日（自動削除）

**内容例**:
```
=== 検査項目: 500行/ファイル制約 ===
実行コマンド: wc -l *.sh *.py *.md
実行時刻: 2026-02-06 02:00:00

=== 実行結果 ===
     182 script.sh
     138 module.py
     320 total

=== 終了コード ===
Exit code: 0
```

---

## 安全性

**全ての検査コマンドは読み取り専用**

| コマンド | 動作 | ファイル変更 |
|---------|------|-------------|
| wc -l | 行数カウント | ❌ なし |
| awk 'length > 80' | 80文字超過検出 | ❌ なし |
| grep 'password' | 機密情報検索 | ❌ なし |
| bash -n | 構文チェック | ❌ なし |

---

## トラブルシューティング

### Gemini APIエラー（429）
- **原因**: RPM/TPM/RPD制限
- **対策**: 自動リトライ（60秒待機、最大3回）

### 深夜帯以外でLevel 3実行
- **対策**: `--force`オプションで強制実行
- **注意**: APIクォータ消費に注意

### launchdが動かない
```bash
# ログ確認
cat ~/100_gemini/020_work_reports/launchd.log
cat ~/100_gemini/020_work_reports/launchd.err

# 再インストール
./105_night_mode/setup_launchd.sh uninstall
./105_night_mode/setup_launchd.sh install
```

---

## 関連ドキュメント

- 計画書: `100_inspection_tools/smart_inspection_self_check_PLAN.md`
- 検査基準: `~/010_STP_APIv1/080_tps/gemini_inspection_standard_v13.md`
- 品質保証: `~/010_STP_APIv1/080_tps/quality_assurance.md`
- 5S: `~/010_STP_APIv1/080_tps/DIGITAL_CONSTRUCTION_5S.md`

---

STP🔧
