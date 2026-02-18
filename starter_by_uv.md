# uv

- https://docs.astral.sh/uv/
- Rustで書かれたpythonのパッケージ、プロジェクトマネージャー
- 参考
  - [uvだけでPythonプロジェクトを管理する](https://zenn.dev/turing_motors/articles/594fbef42a36ee)

## Install uv

```
$ sudo pip3 install uv
```

```
$ uv python install 3.10
Installed Python 3.10.15 in 2.62s
 + cpython-3.10.15-linux-x86_64-gnu
```

## Initialize project

```
$ uv init starter-by-uv-sample
```

```
$ uv init --no-workspace starter-by-uv-sample
Initialized project `starter-by-uv-sample` at `/home/owner/programming_python/starter-by-uv-sample`
```

```
$ cd starter-by-uv-sample
$ uv sync
```

## Activate

```
$ source .venv/bin/activate

$ python hello.py
Hello from starter-by-uv-sample!
```
