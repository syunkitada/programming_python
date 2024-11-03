# full-stack-fastapi-template

```
$ git clone https://github.com/fastapi/full-stack-fastapi-template.git sample1
```

myrc

```
export SECRET_KEY=secretkey
export FIRST_SUPERUSER_PASSWORD=adminpass
export FRONTEND_HOST=http://192.168.10.121:5173
export VITE_API_URL=http://192.168.10.121:8000

export POSTGRES_SERVER=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=app
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=changethis
```

```
$ source myrc
```

## Start postgres

```
$ sudo docker compose up db
```

## Start frontend

```
$ vim package.json
<    "dev": "vite",
>    "dev": "vite --host 0.0.0.0",
```

```
$ cd sample1
$ npm install
$ npm run dev
```

## Start backend

## DBの初期化

```
$ cd backend
$ python app/backend_pre_start.py

# Run migrations
$ alembic upgrade head

# Create initial data in DB
$ python app/initial_data.py
```

## Start backend

```
$ sudo docker compose stop backend

$ cd backend

$ python3 -m venv .venv
$ pip install .
$ fastapi dev --host 0.0.0.0 app/main.py
```

## Settings

- Pydantic Settings
  - 環境変数をそのまま設定として利用できる仕組み
  - backend/app/core/config.py
  - 参考
    - [Pydantic Settingsのすゝめ](https://qiita.com/inetcpl/items/b4146b9e8e1adad239d8)

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
