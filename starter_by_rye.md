# Starter by Rye

- [一般的なパッケージングについて](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Rryを使ったパッケージングについて](https://rye.astral.sh/guide/basics/)
  - 参考: [Rye & uv 時代の Python プロジェクト管理系ツールまとめ](https://zenn.dev/mtkn1/scraps/44ab97ba2dc0a6)
  - Ryeを使うのがいまどきっぽい

## Install Rye

```
wget https://github.com/astral-sh/rye/releases/latest/download/rye-x86_64-linux.gz
gunzip rye-x86_64-linux.gz
chmod +x ./rye-x86_64-linux
sudo mv rye-x86_64-linux /usr/local/bin/rye
```

## Initialize project

```
$ rye init starter-by-rye-sample
```

```
$ cd starter-by-rye-sample
$ curl -Lo ./.gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

$ tree
.
├── README.md
├── pyproject.toml
└── src
    └── starter_by_rye
        └── __init__.py
```

```
$ rye pin 3.10
```

## Define dependencies

```
$ vim pyproject.toml
```

```
[project]
dependencies = [
    "ansible-lint"
]

[tool.rye]
managed = true
dev-dependencies = [
    "ruff",
    "pytest",
]
```

```
$ rye sync

# dev-dependenciesを含めたくない場合は以下を実行する
$ rye sync --no-dev
```

## Initialize project at subsequent times

```
$ rye sync
```

## Activate

```
$ source .venv/bin/activate
```
