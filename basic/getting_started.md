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

- linter, formatter には、black がオススメです
  - https://github.com/psf/black
  - https://black.readthedocs.io/en/stable/integrations/editors.html
  - django とかもこれを使ってる
