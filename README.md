# FastAPI

## ローカル環境構築

### PostgreSQLの起動とpgAdminでの接続
```
% docker compose up -d

% docker ps
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS          PORTS                         NAMES
e453ab66da3c   dpage/pgadmin4:6.3   "/entrypoint.sh"         13 minutes ago   Up 13 minutes   0.0.0.0:80->80/tcp, 443/tcp   fastapi-pgadmin4
d23e0779bd47   postgres:14.1        "docker-entrypoint.s…"   13 minutes ago   Up 13 minutes   0.0.0.0:5432->5432/tcp        fastapi-postgres

% docker inspect fastapi-postgres
(結果を一部抜粋)
"NetworkSettings": {
    "Networks": {
        "fastapi_default": {
            "IPAMConfig": null,
            "Links": null,
            "Aliases": [
                "fastapi-postgres",
                "postgres",
                "d23e0779bd47"
            ],
            "Gateway": "192.168.112.1",
            "IPAddress": "192.168.112.2",
            "IPPrefixLen": 20,
            "IPv6Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "DriverOpts": null
        }
    }
}

上記のIPAddressに接続するようにpgAdminで設定する。この場合は以下のような設定になる。
ホスト名/アドレス: 192.168.112.2
ポート番号: 5432
管理用データベース: fastapi
ユーザ名: root
パスワード: root
```

### DBマイグレーションの実行
```
(fastapiスキーマを作成しておく)
% cd alembic
% alembic upgrade head
```

### Gitのコミット時のチェック設定
```
% pre-commit install
```

※ pre-commitのチェックを実行する場合
```
% pre-commit run --all-files
```

### APIの起動
src/main.py を実行後  
http://127.0.0.1:8000/docs にアクセス

## コードフォーマット(importのソートの自動修正)
```
% pipenv run code-format
```

## テストの実行
```
% pipenv run test
```

## 新しいリビジョンのマイグレーションスクリプト作成
```
% cd alembic
% alembic revision -m "{message}"
```
