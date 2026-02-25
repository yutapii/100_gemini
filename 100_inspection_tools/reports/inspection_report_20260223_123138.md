## 鋼鉄の関門 (v3.2) 検査レポート
**対象**: ../050_WFF
**実施日時**: 2026-02-23 12:31

### 1. 規律遵守状況
| ファイル | 行数 (MAX 500) | 80文字超 (MAX 0) | 判定 |
| :--- | :---: | :---: | :---: |
| calculate_coordinates.py | 303 | 0 | ✅ |
| generate_site_balanced.py | 247 | 0 | ✅ |
| generate_site_swap.py | 426 | 0 | ✅ |
| update_ab_label.py | 29 | 0 | ✅ |
| generate_site_clockwise.py | 251 | 0 | ✅ |
| generate_site_detailed_v3.py | 242 | 0 | ✅ |
| generate_site_measured.py | 385 | 0 | ✅ |
| generate_site_existing_cd90.py | 388 | 0 | ✅ |
| generate_site_optimized.py | 336 | 0 | ✅ |
| generate_site_existing.py | 356 | 0 | ✅ |
| generate_site_clock.py | 399 | 0 | ✅ |
| transform_coordinates.py | 448 | 0 | ✅ |
| read_measurement_pdf.py | 111 | 0 | ✅ |
| read_pdf_with_gemini.py | 92 | 0 | ✅ |
| generate_site_final.py | 316 | 0 | ✅ |
| generate_site_d90.py | 417 | 0 | ✅ |
| add_dimensions.py | 39 | 0 | ✅ |
| verify_edge_lengths.py | 40 | 0 | ✅ |
| generate_site_clockwise_fixed.py | 388 | 0 | ✅ |
| generate_a4_site_plan.py | 309 | 0 | ✅ |
| email_archiver.py | 483 | 0 | ✅ |
| email_html_gen.py | 184 | 0 | ✅ |
| gmail_schedule.py | 285 | 0 | ✅ |
| gmail_cli.py | 114 | 0 | ✅ |
| convert_txt_to_html.py | 166 | 0 | ✅ |
| gmail.py | 488 | 0 | ✅ |
| wff_gmail.py | 218 | 0 | ✅ |
| main.js | 216 | 3 | ❌ |
| vendor_5b_helpers.js | 99 | 0 | ✅ |
| vendor_5a_sections.js | 325 | 0 | ✅ |
| vendor_1b_budget.js | 228 | 0 | ✅ |
| vendor_5_vendors.js | 120 | 0 | ✅ |
| vendor_3_pending.js | 77 | 0 | ✅ |
| vendor_5a_card.js | 464 | 0 | ✅ |
| vendor_6_touki.js | 201 | 0 | ✅ |
| vendor_2_road.js | 89 | 0 | ✅ |
| vendor_4_roadmap.js | 203 | 0 | ✅ |
| app.js | 287 | 0 | ✅ |
| vendor_management.py | 483 | 0 | ✅ |
| vendor_1_property.js | 294 | 0 | ✅ |
| fax_send.py | 163 | 0 | ✅ |
| touki_render.js | 454 | 0 | ✅ |
| loader.py | 82 | 0 | ✅ |
| loader.js | 53 | 0 | ✅ |
| gmail_send_ohara.sh | 7 | 1 | ❌ |
| verify_year50_calculation.py | 155 | 0 | ✅ |
| rent_per_unit_calculation.py | 152 | 0 | ✅ |
| monthly_rent_calculation.py | 141 | 0 | ✅ |
| gmail_send_times.sh | 7 | 0 | ✅ |
| contacts.py | 235 | 0 | ✅ |
| contacts_auth.py | 53 | 0 | ✅ |
| send_fax.py | 170 | 0 | ✅ |
| server.py | 383 | 0 | ✅ |
| start_server.sh | 37 | 0 | ✅ |
| server_file_handlers.py | 274 | 0 | ✅ |
| server_config.py | 100 | 0 | ✅ |
| send_gmail.py | 154 | 0 | ✅ |
| oauth_qr.py | 67 | 0 | ✅ |
| gcal_update.py | 233 | 0 | ✅ |
| gcal_add.py | 112 | 0 | ✅ |
| gcal_list.py | 109 | 0 | ✅ |
| oauth_relay.py | 90 | 0 | ✅ |
| verify_render.js | 180 | 0 | ✅ |

### 2. セキュリティ・機密性
| 項目 | 状態 | 詳細 |
| :--- | :---: | :--- |
| .gitignore | ✅ | 040_security が除外されています |
| 秘密情報 | ⚠️ | 96 件のキーワードが検出されました（要目視確認） |

### 3. メンテナンス性・構造
- **機能フォルダ数**: 69 (1機能1番号1フォルダの原則)
- **設定分離**: ✅ config フォルダによるロジックと設定の分離が確認されました

---
### 最終判定
**判定: 不合格 (再検査が必要)**

Gemini🔍 (鋼鉄の関門 v3.2)
