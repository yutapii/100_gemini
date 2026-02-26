## 鋼鉄の関門 (v3.2) 検査レポート
**対象**: ../090_SUM
**実施日時**: 2026-02-23 11:29

### 1. 規律遵守状況
| ファイル | 行数 (MAX 500) | 80文字超 (MAX 0) | 判定 |
| :--- | :---: | :---: | :---: |
| parse.py | 229 | 0 | ✅ |
| amazon_pdf_auto.py | 251 | 1 | ❌ |
| parse.py | 219 | 0 | ✅ |
| parse.py | 251 | 0 | ✅ |
| gmail.py | 485 | 3 | ❌ |
| parse.py | 178 | 0 | ✅ |
| link.py | 256 | 0 | ✅ |
| parse.py | 221 | 0 | ✅ |
| expense_report.py | 261 | 3 | ❌ |
| add_evidence.py | 170 | 3 | ❌ |
| parse.py | 211 | 0 | ✅ |
| ledger.py | 303 | 0 | ✅ |
| get_digital_orders.js | 190 | 13 | ❌ |
| get_kindle_d01.js | 188 | 13 | ❌ |
| get_kindle_subscription_receipts.js | 125 | 6 | ❌ |
| get_kindle_simple.js | 110 | 4 | ❌ |
| get_kindle_receipts.js | 198 | 17 | ❌ |
| amazon_batch.py | 381 | 5 | ❌ |
| save_session.js | 64 | 4 | ❌ |
| get_kindle_unlimited.js | 146 | 12 | ❌ |
| get_kindle_print.js | 161 | 11 | ❌ |
| find_kindle_subscription.js | 137 | 13 | ❌ |
| run_all.py | 38 | 0 | ✅ |
| get_receipts.js | 134 | 9 | ❌ |
| save_receipts.sh | 50 | 0 | ✅ |
| usage_tracker.py | 215 | 0 | ✅ |
| run_pipeline.sh | 53 | 0 | ✅ |
| journal.py | 446 | 0 | ✅ |
| sort_downloads.py | 123 | 0 | ✅ |
| open_pages.py | 70 | 0 | ✅ |
| parse.py | 195 | 0 | ✅ |
| gpu_monitor.py | 220 | 2 | ❌ |
| import_sbi.py | 199 | 0 | ✅ |
| import_all.py | 67 | 0 | ✅ |
| import_dpoint.py | 188 | 0 | ✅ |
| import_amazon.py | 272 | 0 | ✅ |
| convert.py | 257 | 17 | ❌ |
| chart.js | 210 | 0 | ✅ |
| app.js | 389 | 0 | ✅ |
| merge.py | 302 | 0 | ✅ |
| rotate_image.py | 31 | 1 | ❌ |
| screenshot.py | 54 | 1 | ❌ |
| browser_js.py | 49 | 0 | ✅ |
| html2image.py | 83 | 8 | ❌ |
| backup.py | 250 | 0 | ✅ |
| app.js | 274 | 0 | ✅ |
| start_server.sh | 6 | 0 | ✅ |
| main.py | 407 | 0 | ✅ |
| health_check.py | 304 | 6 | ❌ |
| parse.py | 236 | 0 | ✅ |
| remind_csv.py | 298 | 0 | ✅ |
| parse.py | 233 | 0 | ✅ |
| parse.py | 174 | 0 | ✅ |
| parse.py | 219 | 0 | ✅ |
| parse.py | 221 | 0 | ✅ |
| parse.py | 222 | 0 | ✅ |
| oauth_qr.py | 67 | 0 | ✅ |
| download_csv.py | 170 | 2 | ❌ |
| vitalremind_loader.py | 55 | 2 | ❌ |
| comsys_xml_parser.py | 101 | 6 | ❌ |
| comsys_auto.py | 174 | 7 | ❌ |
| medical_aggregator.py | 122 | 6 | ❌ |
| create_and_inspect.sh | 171 | 4 | ❌ |
| parse.py | 173 | 0 | ✅ |
| reports.py | 339 | 0 | ✅ |
| parse.py | 226 | 0 | ✅ |
| parse.py | 159 | 1 | ❌ |
| oauth_relay.py | 90 | 0 | ✅ |
| handler.py | 91 | 0 | ✅ |
| test_handler.sh | 74 | 1 | ❌ |
| parse.py | 208 | 0 | ✅ |
| apply.py | 176 | 0 | ✅ |

### 2. セキュリティ・機密性
| 項目 | 状態 | 詳細 |
| :--- | :---: | :--- |
| .gitignore | ✅ | 040_security が除外されています |
| 秘密情報 | ⚠️ | 75 件のキーワードが検出されました（要目視確認） |

### 3. メンテナンス性・構造
- **機能フォルダ数**: 71 (1機能1番号1フォルダの原則)
- **設定分離**: ✅ config フォルダによるロジックと設定の分離が確認されました

---
### 最終判定
**判定: 不合格 (再検査が必要)**

Gemini🔍 (鋼鉄の関門 v3.2)
