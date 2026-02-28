# 078_oauth_relay - OAuth中継サーバー

認証コードを自動取得してクリップボードにコピー。

## 用途

- OAuth認証完了後のコードを自動取得
- クリップボードに自動コピー

## 使い方

```bash
python 078_oauth_relay/oauth_relay.py
# または
python 078_oauth_relay/oauth_relay.py --port 8888
```

## 動作

1. サーバー起動（http://localhost:8080）
2. 認証完了後、コードが自動取得
3. クリップボードにコピーされる
4. サーバー自動停止
