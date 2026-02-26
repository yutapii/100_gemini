# VitalRemind 固有コード検査結果

**元レポート**: inspection_report_20260224_085516.md
**対象**: ../040_VitalRemind/（固有コードのみ）
**実施日時**: 2026-02-24 08:55
**規律基準**: 鋼鉄の関門 v3.2

---

## 1. 規律遵守状況（VR固有コード 42件）

| 合格 | 不合格 | 合格率 |
|:----:|:------:|:------:|
| 15 | 27 | 36% |

| ファイル | 行数 | 80文字超 | 判定 |
| :--- | :---: | :---: | :---: |
| app.py | 254 | 12 | ❌ |
| test_deep_inspect.py | 64 | 1 | ❌ |
| fill_shobyouteate.py | 169 | 2 | ❌ |
| replace_dates_reportlab.py | 160 | 6 | ❌ |
| detect_grid.py | 83 | 5 | ❌ |
| auto_replace_dates_final.py | 232 | 3 | ❌ |
| fill_by_coordinate.py | 121 | 1 | ❌ |
| test_extract_fields.py | 33 | 1 | ❌ |
| test_kigou_only.py | 74 | 0 | ✅ |
| test_erase_morphology.py | 217 | 6 | ❌ |
| fill_with_layers.py | 226 | 2 | ❌ |
| auto_replace_dates.py | 178 | 7 | ❌ |
| create_202512_image.py | 314 | 0 | ✅ |
| update_申請期間.py | 144 | 4 | ❌ |
| open_pdf_right.sh | 37 | 0 | ✅ |
| extract_text_coordinates.py | 48 | 1 | ❌ |
| auto_replace_dates_v2.py | 213 | 0 | ✅ |
| debug_grid.py | 141 | 3 | ❌ |
| auto_replace_dates_v3.py | 144 | 9 | ❌ |
| create_202512.py | 107 | 4 | ❌ |
| test_申請期間_x.py | 115 | 1 | ❌ |
| test_seinengappi_checkbox.py | 86 | 1 | ❌ |
| test_bangou_x.py | 97 | 1 | ❌ |
| create_shitaga_layer.py | 175 | 1 | ❌ |
| create_202512_pymupdf.py | 114 | 7 | ❌ |
| test_erase_only.py | 180 | 6 | ❌ |
| test_pypdf_fields.py | 43 | 0 | ✅ |
| add_to_calendar.py | 104 | 20 | ❌ |
| delete_duplicates.py | 79 | 1 | ❌ |
| api_keys.sh | 28 | 2 | ❌ |
| 06_error-logger.js | 81 | 0 | ✅ |
| 03_audio-engine.js | 350 | 0 | ✅ |
| 93_5S_VERIFICATION.sh | 268 | 7 | ❌ |
| 04b_medical-validator.js | 149 | 0 | ✅ |
| 01_app-core.js | 259 | 0 | ✅ |
| 11_report.js | 364 | 0 | ✅ |
| 04_training-logic.js | 419 | 0 | ✅ |
| 05_ui-controller.js | 398 | 0 | ✅ |
| 02_storage-manager.js | 183 | 0 | ✅ |
| 99_start_server.sh | 25 | 3 | ❌ |
| reminder_service.py | 128 | 0 | ✅ |
| logging.py | 79 | 0 | ✅ |

---

## 2. セキュリティ・機密性

| 項目 | 状態 | 詳細 |
| :--- | :---: | :--- |
| .gitignore | ✅ | 040_security除外済 |
| 秘密情報 | ⚠️ | 20265件検出（大半はライブラリ） |

**注**: 秘密情報検出数にはpipライブラリ内の
password/token等の一般的キーワードを含む。
VR固有コードでの実際のハードコードは要個別確認。

---

## 3. メンテナンス性・構造

- **機能フォルダ数**: 29
- **設定分離**: ⚠️ 要確認

---

## 判定

**不合格（再検査が必要）**

主因: VR固有コード27/42件が80文字超過。
500行超過は0件。行数は全て規律内。

**改善の焦点**: 80文字ルールの遵守

---

## 外部ライブラリ検査

別ファイル参照:
`inspection_VitalRemind_20260224_libs.md`

---

Gemini🔍 (鋼鉄の関門 v3.2)
