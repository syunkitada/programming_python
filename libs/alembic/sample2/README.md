# alembic: sample2

既存のモデル定義を利用する例。

```
$ rye sync

$ source .venv/bin/activate
```

## 初期化

```
$ alembic init migrations
```

alembic.iniを編集して接続情報(sqlalchemy.url)を修正します。

```
sqlalchemy.url = sqlite:///test.db
```

```
$ alembic revision --autogenerate -m "mail"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'mail'
  Generating /home/owner/programming_python/libs/alembic/sample2/migrations/versions/c76acf732cde_mail.py ...  done
```

すると、勝手にversionファイルが作成され、test.dbが作成される。

```
$ ls test.db
```

注意として、modelの差分を何でも検知してくれるわけではないので、生成されたversionファイルを自分で確認する必要があります。

[What does Autogenerate Detect (and what does it not detect?)](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)
