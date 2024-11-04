# full-stack-fastapi-template

```
$ git clone https://github.com/fastapi/full-stack-fastapi-template.git sample1
$ cd sample1
$ rm -rf .git
```

## 1. DB(postgres)の起動

```
$ sudo docker compose up db -d

# DBのデータを削除する場合は以下を実行して、再度upを実行してください
$ sudo docker compose down db -v
```

## 2. backendのセットアップ

```
$ cd backend

$ uv sync

$ source .venv/bin/activate
```

DBの初期化

```
$ export FIRST_SUPERUSER=admin@example.com
$ export FIRST_SUPERUSER_PASSWORD=adminpass

$ python app/backend_pre_start.py
$ alembic upgrade head
$ python app/initial_data.py
```

backend用の環境変数の設定

```
export SECRET_KEY=secretkey
export FRONTEND_HOST=http://192.168.10.121:5173
```

backendの起動

```
$ fastapi dev --host 0.0.0.0 app/main.py
```

## 3. frontendのセットアップ

```
$ cd frontend
```

外部からアクセスできるように、viteの起動パラメータを修正します。

```
$ sed -i 's/: "vite",/: "vite --host 0.0.0.0",/g' package.json
```

```
$ npm install
```

```
export SECRET_KEY=secretkey
export VITE_API_URL=http://192.168.10.121:8000
```

```
$ npm run dev
```

## 設定ファイル

- 設定値の管理には Pydantic を利用しており、環境変数をそのまま設定として利用しています
- 参考
  - https://docs.pydantic.dev/latest/
  - [Pydantic Settingsのすゝめ](https://qiita.com/inetcpl/items/b4146b9e8e1adad239d8)

backendの設定(backend/app/core/config.py)

```
  26 class Settings(BaseSettings):
  27     model_config = SettingsConfigDict(
  28         # Use top level .env file (one level above ./backend/)
  29         env_file="../.env",
  30         env_ignore_empty=True,
  31         extra="ignore",
  32     )
  33     API_V1_STR: str = "/api/v1"
  34     SECRET_KEY: str = secrets.token_urlsafe(32)
  35     # 60 minutes * 24 hours * 8 days = 8 days
  36     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
  37     FRONTEND_HOST: str = "http://localhost:5173"
  38     ENVIRONMENT: Literal["local", "staging", "production"] = "local"
  ...
  97     FIRST_SUPERUSER: str
  98     FIRST_SUPERUSER_PASSWORD: str
...
 122 settings = Settings()  # type: ignore
```
