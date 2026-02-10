# smart_inspection_self_check.sh 実装計画

## 目的

AIの「やりました詐欺」を完全に防ぐ、証跡ベース品質検査スクリプトの実装

**核心設計**:
```
スクリプト自身がコマンド実行 → 結果を証跡ファイルに記録 → AIは証跡を読んで分析のみ
```

---

## 問題の本質

### 現状の問題
- **Gemini**: ツール実行不可 → 検査せずに「合格」判定（信頼性ゼロ）
- **Claude**: ツール実行可能 → しかし本当に実行したか検証不可能
- **人間**: AIの出力を盲信 → 「やりました詐欺」に騙される可能性

### 解決策（案A: スクリプト自動実行）
```
【深夜帯の動作（完全自動）】
1. 寝る前に実行: ./smart_inspection_self_check.sh
2. スクリプトが自動実行: wc -l, awk, grep, bash -n
3. 検査は全て読み取り専用（ファイルを壊さない）
4. 証跡ファイルに記録
5. AI分析（証跡を読むだけ）
6. 翌朝、レポート確認
```

- **人間の作業**: スクリプト起動のみ（寝る前）
- **スクリプトの役割**: コマンド自動実行 + 証跡記録
- **AIの役割**: 証跡ファイルを読んで分析のみ（実行は任せない）
- **安全性**: 全てのコマンドは読み取り専用（ファイル変更なし）

---

## 安全性の保証

### 全ての検査コマンドは読み取り専用

| コマンド | 動作 | ファイル変更 |
|---------|------|-------------|
| `wc -l *.sh` | 行数カウント | ❌ なし |
| `awk 'length > 80' *.sh` | 80文字超過検出 | ❌ なし |
| `grep 'password' *.sh` | 機密情報検索 | ❌ なし |
| `bash -n script.sh` | 構文チェック（実行しない） | ❌ なし |
| `python -m py_compile script.py` | 構文チェック（.pycのみ作成） | ⚠️ .pyc のみ |

**保証**: 検査対象ファイル（.sh, .py, .md）を一切変更しません。

### 深夜帯の完全自動実行

- **寝る前**: スクリプト起動のみ（1コマンド）
- **深夜帯**: 完全自動実行（ユーザー操作不要）
- **翌朝**: レポート確認のみ

---

## ファイル構成

### 🚨 作業場所の明確化（絶対厳守）

**背任行為の防止**: AIが勝手に作業場所を決めてはならない

```
❌ NG: 無断で他所に作る
   - ~/.claude/plans/ 等の一時ディレクトリ
   - ユーザーに確認せず独断で決定
   - 背任行為

✅ OK: ユーザー指定の場所で作業
   - ~/100_gemini/100_inspection_tools/ （本プロジェクト）
   - 事前に確認・合意を得る
```

### 新規作成ファイル

**配置場所**: `/Users/saitoyutaka/100_gemini/100_inspection_tools/`

- `smart_inspection_self_check.sh` - メインスクリプト（300行以内）
- `smart_inspection_self_check_PLAN.md` - 本計画書
- `README.md` - 使い方ガイド

### 証跡ファイル
- `/Users/saitoyutaka/100_gemini/020_work_reports/evidence/`
  - `evidence_[検査項目]_[YYYYMMDD_HHMM].txt`
  - `evidence_analysis_[YYYYMMDD_HHMM].txt`
  - `evidence_[YYYYMMDD_HHMM]_REPORT.md`

---

## 主要関数設計

### 1. init_evidence_dir()
- 証跡ディレクトリを作成
- タイムスタンプを生成
- 古い証跡（30日以上）を削除

### 2. run_command_with_evidence(item, cmd, desc)
- コマンドを実行
- 結果を証跡ファイルに記録
- タイムスタンプ、コマンド、実行結果、終了コードを記録
- 証跡ファイルパスを返す

### 3. check_500_lines(target_dir)
- `wc -l` を実行（スクリプト自身）
- 500行超過を即座に判定
- 証跡ファイルに保存

### 4. check_80_chars(target_dir)
- `awk 'length > 80'` を実行
- 80文字超過を即座に判定
- 証跡ファイルに保存

### 5. check_secrets(target_dir)
- `grep` で機密情報パターンを検索
- ハードコードされた機密情報を検出
- 証跡ファイルに保存

### 6. check_syntax(target_dir)
- `bash -n` でShell構文チェック
- `python -m py_compile` でPython構文チェック
- 証跡ファイルに保存

### 7. run_gemini_with_retry(model, prompt)
- `smart_inspection_night.sh` の関数を再利用（100-148行）
- max_retries=3, RETRY_WAIT=60秒
- 429エラー検出で自動リトライ

### 8. request_gc_analysis()
- GC（Gemini CLI）に証跡ファイル分析を依頼
- 証跡ファイルパスをプロンプトに含める
- GC分析結果を証跡ファイルに保存

### 9. request_cc_verification()
- CC（Claude Code）にGC分析結果の検証を依頼
- GC分析結果を読ませる
- CC検証結果を証跡ファイルに保存
- GCとCCの相違点を記録

### 10. judge_level(level)
- レベルごとの合否判定
- GCとCCの両方が合格 → 合格
- いずれかが不合格 → 不合格（次レベルへ）

### 11. check_gc_quota()
- GCクォータ状況を確認
- RPM/TPM/RPD制限を検出
- 夜間実行の必要性を判定

### 12. is_night_mode()
- 深夜帯（01:00-05:59）判定
- `smart_inspection_night.sh` から再利用（13-23行）

### 13. send_gmail_report()
- Gmail送信（Yondex方式）
- `/Users/saitoyutaka/000_WhiteTool/070_functions/gmail_sender.sh` を参考
- 件名: [STP] 品質検査完了レポート
- 本文: 検査結果サマリー + 証跡ファイルパス

### 14. generate_report()
- 最終レポートを生成（Markdown形式）
- 検査結果サマリー、GC分析、CC検証、証跡一覧を含む

---

## 実装フロー（3段階エスカレーション + AI相互監視）

### メインフロー
```
1. 初期化
   ├── 証跡ディレクトリ作成
   ├── タイムスタンプ生成
   └── 古い証跡クリーンアップ

2. レベル1：簡易検査
   ├── スクリプト: 4項目検査 → 証跡保存
   │   - 500行制約
   │   - 80文字制約
   │   - 機密情報
   │   - 構文エラー
   ├── GC（Gemini CLI）: 証跡分析 → 証跡保存
   ├── CC（Claude Code）: GC検証 → 証跡保存
   └── 判定: 合格 → 終了 / 不合格 → レベル2へ

3. レベル2：中程度検査（レベル1不合格時）
   ├── スクリプト: 9項目検査 → 証跡保存
   │   - レベル1の4項目
   │   - XSS脆弱性
   │   - セマンティックHTML
   │   - グローバル変数
   │   - コード重複
   │   - アクセシビリティ
   ├── GC: 証跡分析 → 証跡保存
   ├── CC: GC検証 → 証跡保存
   └── 判定: 合格 → 終了 / 不合格 → レベル3へ

4. レベル3：精密検査（夜間のみ・レベル2不合格時）
   ├── GCクォータ確認: RPM/TPM/RPD復旧確認
   ├── 夜間判定: 深夜帯（01:00-05:59）のみ実行
   ├── スクリプト: 13項目検査 → 証跡保存
   │   - レベル2の9項目
   │   - コメント充実度
   │   - 命名規則
   │   - CSSハードコーディング
   │   - コントラスト比
   ├── GC: 証跡分析 → 証跡保存
   ├── CC: GC検証 → 証跡保存
   └── 最終判定: Grade A-F

5. レポート生成 + Gmail送信（夜間のみ）
   ├── 検査結果サマリー
   ├── GC分析結果
   ├── CC検証結果
   ├── 証跡ファイル一覧
   └── **Gmail送信**（夜間帯のみ）: 翌朝通知
```

### 夜間バッチ戦略

**レベル1（簡易）**: いつでも実行可能
- モデル: Flash-Lite（安い・速い）
- 所要時間: 5分以内
- クォータ: 消費少ない
- **Gmail送信**: なし

**レベル2（中程度）**: クォータ確認後実行
- モデル: Flash（中程度）
- 所要時間: 10分程度
- クォータ: GC復旧状況を確認
- **Gmail送信**: なし

**レベル3（精密）**: 夜間のみ実行
- モデル: Pro（高い・遅い）
- 所要時間: 30分以上
- クォータ: 夜間に復旧を待つ
- **Gmail送信**: 必須（翌朝通知）

### Gmail送信機能（夜間帯のみ）

**参考**: `/Users/saitoyutaka/000_WhiteTool/070_functions/gmail_sender.sh`

**送信条件**:
- レベル3実行完了時のみ
- 深夜帯（01:00-05:59）に実行された場合のみ

**送信タイミング**:
- レベル3完了直後
- 夜間バッチ完了直後

**送信内容**:
```
件名: [STP] 品質検査完了レポート (YYYY-MM-DD HH:MM)

本文:
- 検査レベル: レベル3（精密検査）
- 最終判定: Grade A-F
- GC分析: サマリー
- CC検証: サマリー
- 詳細レポート: 証跡ファイルパス
```

**非送信時**:
- レベル1完了: 画面出力のみ
- レベル2完了: 画面出力のみ
- 日中のレベル3: Gmail送信なし（画面出力のみ）

### AI相互監視の仕組み

**GC（Gemini CLI）の役割**:
- 証跡ファイルを読んで一次分析
- 重大度判定、修正提案
- 分析結果を証跡に保存

**CC（Claude Code）の役割**:
- GCの分析結果を検証
- GCのハルシネーション検出
- GCと異なる視点での再分析
- 最終判定

**相互監視の効果**:
- GCとCCは構造が違う → 同じバイアスを持たない
- GCが誤検知 → CCが訂正
- CCが見逃し → GCが別視点で指摘
- 信頼性: 単独AIより高い

---

## 既存コードの再利用

### smart_inspection_night.sh (182行)
- `run_gemini_with_retry()` 関数（100-148行）
  - リトライロジック、RPM/TPM/RPD制限対応
  - そのまま再利用可能

- タイムスタンプ形式
  - `[$(date '+%Y-%m-%d %H:%M:%S')]`
  - 証跡ファイルで同じ形式を使用

### smart_inspection.sh (138行)
- 3段階エスカレーションの設計
  - 参考にするが、今回は単一レベル（Flash-Lite）で実装
  - 将来的に拡張可能な設計にする

### gemini_auto_retry.sh (72行)
- エラー検出パターン
  - "429|RESOURCE_EXHAUSTED|capacity"
  - 同じパターンを使用

---

## 制約・品質基準

### デジタル建築5S準拠
- **500行/ファイル**: スクリプト本体を300行以内に設計
- **80文字/行**: 全行80文字以内（罫線削除）
- **削除禁止**: 旧バージョンは999_trash/へ退避
- **バックアップ必須**: 実装前にスナップショット作成

### 品質保証（7ステップ）
1. **契約**: この計画をユーザーに提示し合意
2. **実装**: 計画通りに実装（勝手な追加禁止）
3. **復唱**: 実装内容を復唱し、計画との差分を報告
4. **自己テスト**: bash -n で構文チェック、実行テスト
5. **GCテスト**: Geminiで辛辣チェック
6. **Claude判断**: Gemini指摘を検証し、同意/反論
7. **合意形成**: ユーザー承認を得て完了

---

## 段階的実装

### Step 1: 最小実装（証跡記録のみ）
**目標**: スクリプト自身がコマンド実行し、証跡ファイルに保存

**実装範囲**:
- `init_evidence_dir()`
- `run_command_with_evidence()`
- `check_500_lines()`
- メインフロー（検査1つのみ）

**テスト**:
```bash
./smart_inspection_self_check.sh ~/100_gemini/010_ai
ls -lh ~/100_gemini/020_work_reports/evidence/
cat ~/100_gemini/020_work_reports/evidence/evidence_*_500lines.txt
```

**成功条件**:
- 証跡ファイルが作成される
- コマンド実行結果が記録されている
- タイムスタンプが正しい

---

### Step 2: 4検査実装（AI分析なし）
**目標**: 4つの検査が証跡記録できる

**実装範囲**:
- `check_80_chars()`
- `check_secrets()`
- `check_syntax()`
- メインフロー（4検査すべて）

**テスト**:
```bash
./smart_inspection_self_check.sh --no-ai ~/100_gemini/010_ai
ls -lh ~/100_gemini/020_work_reports/evidence/
```

**成功条件**:
- 4つの証跡ファイルが作成される
- 各検査の判定（✅/⚠️）が正しい
- 証跡ファイルが人間が読める形式

---

### Step 3: AI相互監視実装
**目標**: GCとCCの相互監視が動作する

**実装範囲**:
- `run_gemini_with_retry()`（再利用）
- `request_gc_analysis()`
- `request_cc_verification()`
- `judge_level()`
- レベル1のみ実装

**テスト**:
```bash
./smart_inspection_self_check.sh ~/100_gemini/010_ai
cat ~/100_gemini/020_work_reports/evidence/evidence_*_gc_analysis.txt
cat ~/100_gemini/020_work_reports/evidence/evidence_*_cc_verification.txt
```

**成功条件**:
- GC分析が成功する
- CC検証が成功する
- GCとCCの相違点が記録される
- 合否判定が正しい

---

### Step 4: 3段階エスカレーション実装
**目標**: レベル1→2→3のエスカレーションが動作する

**実装範囲**:
- レベル2の検査関数
- レベル3の検査関数
- エスカレーションロジック

**テスト**:
```bash
# レベル1不合格のファイルで実行
./smart_inspection_self_check.sh [不合格ファイル]
# レベル2→3へエスカレーションされることを確認
```

**成功条件**:
- レベル1不合格 → レベル2へエスカレーション
- レベル2不合格 → レベル3へエスカレーション
- 各レベルでGC+CC相互監視が動作

---

### Step 5: 完成形（レポート生成・夜間バッチ）
**目標**: 完全動作 + 夜間バッチ対応

**実装範囲**:
- `generate_report()`
- `cleanup_old_evidence()`
- 夜間バッチ対応（nohup または深夜帯待機）

**テスト**:
```bash
# 夜間バッチテスト
nohup ./smart_inspection_self_check.sh ~/100_gemini/010_ai &
# 翌朝レポート確認
cat ~/100_gemini/020_work_reports/evidence/evidence_*_REPORT.md
```

**成功条件**:
- 夜間バッチが動作する
- 最終レポートが生成される
- レポートにGC+CCの分析が含まれる

---

## 検証方法

### 証跡ファイルの確認
```bash
# 証跡ディレクトリの構造確認
tree ~/100_gemini/020_work_reports/evidence/

# 最新の証跡を確認
ls -lt ~/100_gemini/020_work_reports/evidence/ | head -10

# 特定の検査項目を確認
cat ~/100_gemini/020_work_reports/evidence/evidence_*_80chars.txt
```

### 手動検証（証跡との照合）
```bash
# 被検査側で手動実行
cd ~/100_gemini/010_ai
wc -l *.sh *.py *.md  # 証跡ファイルと照合
awk 'length > 80' *.sh  # 証跡ファイルと照合
```

### 期待される証跡ファイル形式
```
=== 検査項目: 500行/ファイル制約（wc -l実行） ===
実行コマンド: cd ~/100_gemini/010_ai && wc -l *.sh *.py *.md
実行時刻: 2026-02-06 13:00:00

=== 実行結果 ===
     182 smart_inspection_night.sh
     138 smart_inspection.sh
      72 gemini_auto_retry.sh
     392 total

=== 終了コード ===
Exit code: 0
```

---

## 「やりました詐欺」防止設計

### 信頼チェーン
```
【信頼できる】
スクリプト自身がコマンド実行
    ↓
証跡ファイルに記録（タイムスタンプ付き）
    ↓
人間が後で検証可能

【信頼できない】
AI「コマンド実行しました」← 本当に実行したか不明
```

### AIの役割の制限
```
❌ AIに任せない:
  - コマンド実行
  - 結果の捏造
  - 推測による判定

✅ AIに任せる:
  - 証跡ファイルの読み取り
  - 解釈・重大度判定
  - 修正提案
```

---

## Critical Files

実装に必要な重要ファイル:

1. **`/Users/saitoyutaka/100_gemini/010_ai/smart_inspection_night.sh`** (182行)
   - `run_gemini_with_retry()` 関数（100-148行）を再利用
   - `is_night_mode()` 関数（13-23行）を再利用

2. **`/Users/saitoyutaka/100_gemini/010_ai/smart_inspection.sh`** (138行)
   - 3段階エスカレーション設計を参考

3. **`/Users/saitoyutaka/010_STP_APIv1/080_tps/DIGITAL_CONSTRUCTION_5S.md`** (194行)
   - 80文字/500行制約、5S定義を厳守

4. **`/Users/saitoyutaka/010_STP_APIv1/080_tps/quality_assurance.md`** (283行)
   - 完了7ステップ、品質保証手順を遵守

5. **`/Users/saitoyutaka/000_WhiteTool/070_functions/gmail_sender.sh`**
   - Gmail送信機能の参考実装（Yondex方式）

---

## 実装時の注意事項

### NEVER（絶対にやらないこと）
```
❌ AIにコマンド実行を任せる
❌ 証跡ファイルをAIに書かせる
❌ 推測・憶測で判定する
❌ 罫線で80文字超過させる
❌ 500行を超える
❌ 既存スクリプトを削除する（999_trash/へ退避）
```

### ALWAYS（必ずやること）
```
✅ スクリプト自身がコマンド実行
✅ 証跡ファイルにタイムスタンプ記録
✅ 人間が後で検証可能にする
✅ 既存関数を再利用する
✅ 80文字/行を厳守
✅ 500行/ファイルを厳守
✅ 実装前にバックアップ作成
```

---

## 📊 Phase間フィードバックループ（計画実行制御）

### 根本原則

**「計画通りの実行」を保証するため、各Phase完了後に証跡ベース判定を実施**

### フィードバックサイクル

```
Phase N実施
    ↓
証跡収集（101_evidence_collector/）
    ↓
Gemini分析（102-104_inspector_*/）
    ↓
CC検証（108_cc_verifier/）
    ↓
判定結果に基づき次Phase実施判断
    ↓
Phase N+1実施 or 修正 or ユーザー確認
```

### Phase完了後の判定基準

**判定パターン**:

1. **Phase完了 + 問題なし + 次Phase必要**
   → 次Phaseを実施

2. **Phase完了 + 問題あり**
   → 修正後、当該Phase再実施

3. **Phase完了 + 次Phase不要**
   → Phase完了報告、作業終了

4. **Phase完了 + 判定不明**
   → ユーザー確認

### 判定実施手順

**1. 証跡収集**
```bash
cd ~/100_gemini/101_evidence_collector
./collect_evidence.sh [対象DIR] > /tmp/phase_N_evidence.log
```

**2. Gemini分析**
```bash
gemini --model "gemini-2.5-flash" "
Phase N証跡を分析し、Phase N+1の必要性を判定してください。

【証跡】
$(cat /tmp/phase_N_evidence.log)

【判定基準】
1. Phase Nで問題発見 → Phase N+1必須
2. システムが複雑 → 次Phase必要
3. 手動運用で十分 → 次Phase不要

【出力】
Phase N+1: 必要/不要
理由: [具体的根拠]
"
```

**3. CC検証**
```bash
cd ~/100_gemini/108_cc_verifier
./verify_gemini.sh [Geminiレポート] [証跡DIR] [対象DIR]
```

**4. 判定結果に基づく実施**
- Gemini「必要」+ CC「一致」→ 次Phase実施
- Gemini「不要」+ CC「一致」→ 作業完了
- Gemini vs CC 不一致 → ユーザー確認

### AI独断の防止

**❌ NEVER**:
- AIが主観で「次Phaseは不要」と判断
- 証跡ベース判定を省略
- Gemini分析なしに進行

**✅ ALWAYS**:
- 各Phase完了後、必ずGemini分析を実施
- CC検証で実証確認
- 判定結果に基づき次ステップ決定

---

## 実装スケジュール

1. **Step 1実装**: 最小実装（証跡記録のみ）→ テスト → 確認
2. **Step 2実装**: 4検査実装 → テスト → 確認
3. **Step 3実装**: AI分析・レポート生成 → テスト → 確認
4. **品質保証**: 7ステップ完了 → ユーザー承認

**推定工数**: Step 1-3 各30分、品質保証30分、合計2時間

---

## 🔍 計画内容の点検プロセス（義務化）

### 実装前の品質保証

**計画内容自体もCC+GCで相互点検する**

```
1. プランファイル作成（CC）
   ↓
2. GC点検: プランファイルを読んで点検
   - 実装可能性
   - 制約違反（80文字/500行）
   - 論理的矛盾
   - 抜け漏れ
   ↓
3. CC検証: GC点検結果を検証
   - GCの指摘は妥当か
   - GCが見逃した問題はないか
   - 計画修正の必要性
   ↓
4. ユーザー最終承認
```

### 点検項目

**GCが点検すべき項目**:
- [ ] 実装可能性（技術的に実現可能か）
- [ ] 制約遵守（80文字/500行/5S）
- [ ] 論理的整合性（矛盾はないか）
- [ ] 完全性（抜け漏れはないか）
- [ ] セキュリティ（機密情報漏洩リスク）
- [ ] エラーハンドリング（異常系の考慮）

**CCが検証すべき項目**:
- [ ] GC点検の妥当性（誤検知・見逃し）
- [ ] GCと異なる視点での問題発見
- [ ] 実装優先度の確認
- [ ] テスト戦略の妥当性

### 点検実施方法

**Step 1: GC点検**
```bash
cat /Users/saitoyutaka/.claude/plans/declarative-puzzling-bubble.md | \
  gemini "このプランファイルを点検してください。

点検項目:
- 実装可能性
- 制約遵守（80文字/500行）
- 論理的整合性
- 完全性
- セキュリティ
- エラーハンドリング

辛辣に指摘してください。"
```

**Step 2: CC検証**
- GC点検結果を読む
- GC指摘の妥当性を検証
- GCが見逃した問題を指摘
- 計画修正の必要性を判断

**Step 3: 計画修正**
- CC+GCの指摘を反映
- プランファイル更新

**Step 4: ユーザー承認**
- 修正後の計画を提示
- ExitPlanMode で承認を求める

---

STP🔧
