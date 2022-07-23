# testing

- python でテストを行うための手段は、doctest、unittest、pytest があるが、ここでは pytest のみを扱う
  - pytest は、unittest とできることはだいたい同じだが、unittest よりも記述が簡易で扱いやすく、いくつかの便利機能が追加されている
    - 世間一般的にも pytest のほうが使われてる（気がする）
  - doctest は、docstring 内にテストコードを書くものだが、docstring 内にテストコードが分散するとわかりずらいため使わない

## ディレクトリ構成

- メインのプログラムを管理するディレクトリとは別に、tests ディレクトを作成し、その配下にまったく同じディレクト構成でテストファイルを作成する
- テストファイルの命名規則は、'test\_[module name].py' とする

```
- pkg
  - hello.py
- tests
  - test_hello.py
```

```
- pkg
  - mod1
    - hello.py
- tests
  - mod1
    - test_hello.py
```
