# VitalRemind 外部ライブラリ検査サマリー

**元レポート**: inspection_report_20260224_085516.md
**対象**: ../040_VitalRemind/ 内pipライブラリ
**実施日時**: 2026-02-24 08:55

---

## 概要

検査スクリプトがvenv/site-packages配下の
外部ライブラリも含めてスキャンした結果。

**これらは修正対象外**（サードパーティコード）。

---

## 統計

| 項目 | 件数 |
|:-----|-----:|
| スキャン対象 | 1425 |
| 合格（✅） | 478 |
| 不合格（❌） | 947 |
| 合格率 | 34% |

---

## 主なライブラリと状況

| ライブラリ | 代表的な違反 |
|:-----------|:-------------|
| Flask | app.py 1536行、cli.py 1135行 |
| Werkzeug | routing.py等 多数 |
| Jinja2 | compiler.py等 |
| pyasn1 | decoder.py 2207行（最大） |
| oauthlib | 多数のOAuth実装 |
| google-api | discovery.py 1669行 |

---

## 教訓（検査改善への提案）

検査スクリプト `inspect_v3_iron_gate.sh` の
findコマンドに以下の除外を追加すべき:

```bash
-not -path "*/venv/*"
-not -path "*/.venv/*"
-not -path "*/site-packages/*"
```

理由: 外部ライブラリはWT規律の管轄外。
スキャンするとレポートが肥大化し、
VR固有コードの問題が埋もれる。

---

Gemini🔍 (鋼鉄の関門 v3.2 / 参考資料)
