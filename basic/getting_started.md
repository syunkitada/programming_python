# Getting Started

## どのバージョン使えばよいか？

- ダウンロードページ
  - [https://www.python.org/downloads/](https://www.python.org/downloads/)
- リリースサイクルは毎年で、各サポート期間は 5 年
- 最新バージョン-1 か -2 を使うと良い
  - 最新バージョンを使ってしまうとライブラリが対応してない場合が多いので避ける
  - 基本的に OS でサポートしてるバージョンをそのまま使うのが推奨

## ライブラリ依存を venv で管理するか、OS 側のパッケージマネージャで管理するか？

- 基本的には venv 側でよいが、python 外の共有ライブラリに依存したものは OS 側のパッケージマネージャで管理するのがよい
  - 外の共有ライブラリに依存してるというのは、pip install の時に、xxx-dev, xxx-devel などを要求してくるもの
  - このようなライブラリは、OS 側のライブラリへのリンクの都合上、OS 側のライブラリのバージョンに依存してしまう
  - もし、このようなライブラリを venv 側にインストールしてしまうと、その依存として OS 側のライブラリのバージョンを適切に管理する必要が出てくる
    - OS 側のパッケージマネージャで管理する場合は、その python ライブラリを OS 側でインストールするだけでよい（バージョンを意識しなくてよい）

## 環境構築

- 各プロジェクトごとに venv という名前の venv を作って依存はそこにインストールします

```
$ sudo apt install -y python3 python3-venv python3-dev python3-pip

$ python3 --version
Python 3.8.10

# 以下は各プロジェクトのルートで外部ライブラリを利用する場合に実行します
$ python3 -m venv venv

# OS側のライブラリ群も利用する場合は --system-site-packages オプションをつけて実行します
$ python3 -m venv --system-site-packages venv

$ source venv/bin/activate

# 依存は、requirements.txtで管理します
$ vim requirements.txt
...

$ pip install -r requirements.txt
```

- 上記の簡易版として各プロジェクトごとに（依存がある場合は）Makefile に環境構築処理を書いておき、以下のコマンドで構築できるようにします

```
$ make env
$ source venv/bin/activate
```

## 開発環境の補足

- linter
  - flake8
  - 設定ファイルは、pyproject.toml ではなく、tox.ini, setup.cfg, .pep8, .flake8 のいずれか
- formatter
  - black
    - https://github.com/psf/black
    - https://black.readthedocs.io/en/stable/integrations/editors.html
    - django とかもこれを使ってる
    - 設定ファイルは、setup.cfg ではなく、pyproject.toml なので注意
  - isort
    - https://pycqa.github.io/isort/
    - import 分をソートしてくれる
    - black と併用すると良い
  - max-line-length について
    - 既存の制限(2023/03/06 時点)
      - PEP8 は、79 文字
      - black は、88 文字
      - 昔の Django は、119 文字
        - https://github.com/django/django/blob/stable/3.2.x/setup.cfg#L64
        - [昔の GitHub の横幅が 119 文字のため](https://github.com/django/django/blob/stable/3.2.x/docs/internals/contributing/writing-code/coding-style.txt#L52-L58)
          - 今の GitHub は 119 文字というわけではないので気にしなくてよい
        - 今の Django は black の 88 文字にしてる
          - 119 文字の時は black は使われておらず、black 導入時にこれに合わせたと思われる
      - pycharm や vscode は、120 文字
    - 考え方
      - チームで合意が取れてばなんでもよいが長すぎはやめたほうがよい(最大でも 120 が妥当と思われる)
        - 視覚障碍者を考慮するのであれば、100 文字を超えると作業が難しくなるらしいので、最大でも 99 文字に抑えるとよい
      - 基本的には画面にファイルを二つ横に並べて、左にある程度のスペースが残るぐらいが理想と思われる
        - black の 88 文字も、一般解像度でのファイル横並びや、差分レビューを考慮した長さである
      - 悩むぐらいなら、とりあえず black にあわせておくのがよい
