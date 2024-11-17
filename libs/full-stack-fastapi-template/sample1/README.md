# full-stack-fastapi-template: sample1

## 初期化設定の手順

### 1. templateをgit cloneする

```
$ git clone https://github.com/fastapi/full-stack-fastapi-template.git sample1
$ cd sample1
```

originを書き換える。

```
$ git remote set-url origin git@github.com:octocat/my-full-stack.git
```

もしくは、.gitを削除して初期化する。

```
$ rm -rf .git
```

### 2. DB(postgres)の起動

```
$ sudo docker compose up db -d

# DBのデータを削除する場合は以下を実行して、再度upを実行してください
$ sudo docker compose down db -v
```

### 3. backendのセットアップ

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

### 4. frontendのセットアップ

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

## 設定ファイルについて

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

## backendのテスト

```
$ cd backend
$ python app/tests_pre_start.py
$ ./scripts/test.sh

============================================================== 54 passed, 5 warnings in 16.24s ===============================================================
+ coverage report --show-missing
Name                                          Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------
app/__init__.py                                   0      0   100%
app/api/__init__.py                               0      0   100%
app/api/deps.py                                  35      4    89%   36-37, 43, 45
app/api/main.py                                   7      0   100%
app/api/routes/__init__.py                        0      0   100%
app/api/routes/items.py                          57      4    93%   27-39
app/api/routes/login.py                          57      9    84%   37, 88, 93, 110-122
app/api/routes/users.py                         102      0   100%
app/api/routes/utils.py                          14      4    71%   20-26, 31
app/backend_pre_start.py                         23      7    70%   27-29, 33-35, 39
app/core/__init__.py                              0      0   100%
app/core/config.py                               70      4    94%   21-23, 109
app/core/db.py                                   10      0   100%
app/core/security.py                             16      0   100%
app/crud.py                                      40      0   100%
app/initial_data.py                              14     14     0%   1-23
app/main.py                                      14      1    93%   15
app/models.py                                    60      0   100%
app/tests/__init__.py                             0      0   100%
app/tests/api/__init__.py                         0      0   100%
app/tests/api/routes/__init__.py                  0      0   100%
app/tests/api/routes/test_items.py               81      0   100%
app/tests/api/routes/test_login.py               50      0   100%
app/tests/api/routes/test_users.py              263      0   100%
app/tests/conftest.py                            30      0   100%
app/tests/crud/__init__.py                        0      0   100%
app/tests/crud/test_user.py                      72      0   100%
app/tests/scripts/__init__.py                     0      0   100%
app/tests/scripts/test_backend_pre_start.py      16      2    88%   24-25
app/tests/scripts/test_test_pre_start.py         16      2    88%   24-25
app/tests/utils/__init__.py                       0      0   100%
app/tests/utils/item.py                          13      0   100%
app/tests/utils/user.py                          30      1    97%   46
app/tests/utils/utils.py                         15      0   100%
app/tests_pre_start.py                           23      7    70%   27-29, 33-35, 39
app/utils.py                                     64      7    89%   48-49, 53, 59-65
---------------------------------------------------------------------------
TOTAL                                          1192     66    94%
+ coverage html --title coverage
Wrote HTML report to htmlcov/index.html
```
