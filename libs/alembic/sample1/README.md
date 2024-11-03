# alembic: sample1

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

最初のバージョンのモデルを作成します。

```
$ alembic revision -m "init"
  Generating /home/owner/programming_python/libs/alembic/sample1/migrations/versions/c9f6fd37225d_init.py ...  done
```

upgrade, downgradeを以下のように編集します。

```
$ vim migrations/versions/c9f6fd37225d_init.py
```

```
def upgrade() -> None:
    op.create_table(
        "mail",
        sa.Column("id", sa.Integer(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("mail")
```

以下のコマンドでDBスキーマを適用できます。

```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> c9f6fd37225d, init
```

データベーススキーマを更新したい場合は、新しいrevisionを生成し、upgrade, downgradeを修正します。

```
$ alembic revision -m "add a age col"
  Generating /home/owner/programming_python/libs/alembic/sample1/migrations/versions/d589925f76f2_add_a_age_col.py ...  done
```

```
$ vim migrations/versions/d589925f76f2_add_a_age_col.py
```

```
def upgrade() -> None:
    op.add_column("mail", sa.Column("age", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("mail", "age")
```

再度、以下のコマンドでDBスキーマを適用できます。

```
$ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade c9f6fd37225d -> d589925f76f2, add a age col
```
