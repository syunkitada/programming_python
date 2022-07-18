# fabric

- fabric とは、SSH を介してシェルコマンドなどをタスクとして定義して実行できるタスクランナーです
- 各種ドキュメント類
  - [fabric: ドキュメント](https://www.fabfile.org/)
  - [fabirc: コード](https://github.com/fabric/fabric)
  - [invoke: ドキュメント](https://www.pyinvoke.org/)
  - [invoke: コード](https://github.com/pyinvoke/invoke)

## v1, v2 の違い

- fabric v1 は、一時期 Python 3 対応ができておらず、非公式に Python 3 対応のフォークである Fabric3 というものが開発されてしまうという状況でした
  - このため Fabric3 の利用は非推奨です
  - fabric v1 も利用はできますが今後サポートされないので非推奨です
- fabric v2(version 2.0 以降) は、v1 を Python3 対応する際にすべて書き直されており、まったくの別物（非互換）となってることに注意してください
  - v1 を使ってた人は、v1 の感覚で触るのではなくて、別物のフレームワークを使うのだと思ってください
  - 最初触ったときは v1 に比べてデグレしたように見えるかもしれませんが、使い勝手が変わっただけで機能的な違いはほとんどないと思います
- 主な違いとしては、v1 では、スクランナーの実装が fabric 側にありましたが、v2 ではタスクランナーの実装が invoke という別プロジェクトで管理されいます
  - invoke 自体は SSH 周りの実装はなくただのローカルで動くタスクランナーです
  - また、invoke は fabric v1 からインスピレーションを得て作られており、fabric v1 の使用感ととても似ています
- 基本的に SSH 周りは fabric 側で管理されますが、タスクの周りは invoke 側なので、利用箇所によって両者のドキュメントを読む必要があります

## テスト用環境の準備

```
$ make env

$ ssh 10.100.100.2 hostname
host1.example.com

$ source venv/bin/activate

$ fab -l
...

# テストが終わったら以下を実行して環境を破棄する
$ make clean
```

## 基本

### helloworld

- 以下は、hostname を実行するだけのサンプル
- c.run は、remote でコマンドが実行されます
- run, c.local は、local でコマンドが実行されます
- 引数の c は、fabric.connection.Connection です

```
from fabric import task
from invoke import run

@task
def helloworld(c):
    print("c is {}".format(type(c)))
    run("hostname")
    c.local("hostname")
    c.run("hostname")
```

- -H オプションでホストを指定してタスクを実行できます

```
$ fab -H 10.100.100.2 helloworld
c is <class 'fabric.connection.Connection'>
owner-desktop
owner-desktop
host1.example.com
```

- -H オプションでホストを指定しない場合は、ただの invoke として動作します
  - c.local が使えないことに注意してください
- 引数の c は、invoke.context.Context です

```
from fabric import task
from invoke import run

@task
def helloworld2(c):
    print("c is {}".format(type(c)))
    run("hostname")
    c.run("hostname")
```

```
$ fab helloworld2
c is <class 'invoke.context.Context'>
owner-desktop
owner-desktop
```

### タスク定義せずに特定コマンドを実行する

- -- のあとにコマンドを指定すると、タスクを定義しなくても(fabfile がなくても)、特定コマンドを実行することが可能です

```
$ fab -H 10.100.100.2 -- hostname
host1.example.com
```

### 明示的に Connection を作成して、run や特定関数を実行する

```
from fabric import task, Connection
from invoke import run

@task
def hostname(c):
    result = Connection("10.100.100.2").run("hostname")
    result = _hostname(Connection("10.100.100.3"))


def _hostname(c):
    result = c.run("hostname")
```

```
$ fab hostname
host1.example.com
host2.example.com
```

### 複数ホストで直列でタスクを実行する

- シンプルにやるなら-H で, 区切りで複数ホストを指定すれば実行できます

```
$ fab -H 10.100.100.2,10.100.100.3 helloworld
c is <class 'fabric.connection.Connection'>
owner-desktop
owner-desktop
host1.example.com
c is <class 'fabric.connection.Connection'>
owner-desktop
owner-desktop
host2.example.com
```

- SerialGroup を使うと、明示的に複数ホストを指定してコマンドや関数を実行できます

```
from fabric import task, Connection, SerialGroup
from invoke import run


@task
def hostname_serial_group(c):
    result = SerialGroup("10.100.100.2", "10.100.100.3").run("hostname")
    print("---")
    result = _hostname(SerialGroup("10.100.100.3", "10.100.100.4"))


def _hostname(c):
    result = c.run("hostname")
```

```
$ fab hostname-serial-group
host1.example.com
host2.example.com
---
host2.example.com
host3.example.com
```

### 複数ホストで並列でタスクを実行する

- fabric v1 では、並列でのタスク実行がサポートされていたが、v2 では並列実行ができなっている(将来的にはサポートされるかもしれない？)
- 並列実行したい場合は、2 通りのやり方がある

```
# 以下は直列でしか実行できない
$ fab -H 10.100.100.2,10.100.100.3 helloworld
```

- 1 つ目のやり方は、ThreadingGroup を使うやり方です

```
from random import randint
from time import sleep

from fabric import task, Connection, SerialGroup, ThreadingGroup
from invoke import run


@task
def hostname_threading_group(c):
    result = ThreadingGroup("10.100.100.2", "10.100.100.3").run("hostname")
    print("---")
    result = _hostname_sleep(ThreadingGroup("10.100.100.3", "10.100.100.4"))


def _hostname_sleep(c):
    result = c.run("hostname")
    sleep(randint(1, 5))
    result = c.run("hostname")
```

```
$ fab hostname-threading-group
host2.example.com
host1.example.com
---
host3.example.com
host2.example.com
host2.example.com
host3.example.com
```

- 2 つ目のやり方は、Python 標準の ThreadPool を利用するやり方です
- 1 つ目のやり方では、pool_size の指定ができないため（fabric v1 ではできていた）、並列数は無制限です（たぶん）
- 1 つ目のやり方では、例外時のハンドリングもできません（たぶん）
- 以下のように、ThreadPool を使用すると、pool_size の指定や、例外時のハンドリングをして結果を集約することが可能です

```
from random import randint
from time import sleep
from concurrent.futures import ThreadPoolExecutor

from fabric import task, Connection, SerialGroup, ThreadingGroup
from invoke import run


@task
def hostname_thread_pool(c):
    hosts = ["10.100.100.2", "10.100.100.3", "10.100.100.4"]
    results = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(_hostname_sleep_wrapper, hosts))


def _hostname_sleep_wrapper(host):
    result = None
    err = None
    try:
        result = _hostname_sleep(Connection(host))
    except Exception as e:
        err = e

    return {
        "result": result,
        "err": err,
    }


def _hostname_sleep(c):
    result = c.run("hostname")
    sleep(randint(1, 5))
    result = c.run("hostname")
```

## sudo を使う

- fabric タスクの場合(-H を指定してタスク実行する場合)は、--prompt-for-sudo-password オプションを指定する
  - これにより、c.config に sudo password がセットされるため、パスワードの要求なしで c.sudo が実行可能になる

```
@task
def sudo_hostname(c):
    c.sudo("hostname")
```

```
$ fab --prompt-for-sudo-password -H 10.100.100.2 sudo-hostname
Desired 'sudo.password' config value:
[sudo] password: host1.example.com
```

- fabric タスクでない場合(-H を指定しない場合)は、c.config を Connection（や SerialGroup）に引き継がせる必要があります

```
@task
def sudo_hostname_serial_group(c):
    result = SerialGroup("10.100.100.2", "10.100.100.3", config=c.config).sudo("hostname")
```

```
$ fab --prompt-for-sudo-password sudo-hostname-serial-group
Desired 'sudo.password' config value:
[sudo] password: host1.example.com
[sudo] password: host2.example.com
```

- 実際の利用では、--prompt-for-sudo-password オプションを指定するよりも、タスク内で sudo を使なら明示的にパスワードを入力させたいと思います
- 以下のように、Config を直接定義することが可能です
  - この Config は fabric のですが、これは invoke の Config をラップしたものです
  - ssh 周りの Config は fabric のドキュメントを参照し、run, sudo などの Config は invoke のドキュメントを参照することに注意してください

```
import getpass
from random import randint
from time import sleep
from concurrent.futures import ThreadPoolExecutor

from fabric import task, Connection, SerialGroup, ThreadingGroup, Config
from invoke import run


@task
def sudo_hostname2(c):
    sudo_pass = getpass.getpass("Input your sudo password > ")
    config = Config()
    config['sudo'] = {'password': sudo_pass}
    result = SerialGroup("10.100.100.2", "10.100.100.3", config=config).sudo("hostname")
```

```
$ fab sudo-hostname2
Input your sudo password >
[sudo] password: host1.example.com
[sudo] password: host2.example.com
```

## コマンドの失敗を無視する

- 以下のタスクは、存在しないファイルの存在確認をしているため失敗する

```
@task
def touch_if_not_exists(c):
    print("start")
    c.run("test -e /tmp/hoge")
    print("end")
```

```
$ fab -H 10.100.100.2 touch-if-not-exists
start

$ echo $?
1
```

- 以下のように warn=True とすると、失敗を無視することができます
- また、run の結果が失敗したかどうかを failed で判定できます

```
@task
def touch_if_not_exists2(c):
    print("start")
    if c.run("test -e /tmp/hoge", warn=True).failed:
        c.run("echo 'hoge' > /tmp/hoge")
    else:
        print("already exists")
    c.run("cat /tmp/hoge")
    print("end")
```

```
$ fab -H 10.100.100.2 touch-if-not-exists2
start
hoge
end

$ fab -H 10.100.100.2 touch-if-not-exists2
start
already exists
hoge
end
```

## ファイルを put, get する

```
@task
def get_and_put(c):
    if c.run("test -e /tmp/hoge", warn=True).failed:
        c.run("echo 'hoge' > /tmp/hoge")

    c.get("/tmp/hoge", "/tmp/hoge")
    c.local("cat /tmp/hoge")

    c.put("/tmp/hoge", "/tmp/hoge2")
    c.run("cat /tmp/hoge2")
```

```
$ fab -H 10.100.100.2 get-and-put
hoge
hoge
```

## 実行コマンドやホスト名を表示する

- config で、echo を True、echo_format を定義することで実現できます
  - echo_format で利用できるテンプレート変数は command のみです
  - ホスト名は独自で入れる必要があるため、複数ホストで利用する場合は各ホストごとに config を用意して echo_format を定義する必要があります

```
@task
def get_and_put2(c):
    config = Config()
    echo_config = {"echo": True, "echo_format": "10.100.100.2: {command}"}
    config["run"].update(echo_config)
    config["sudo"].update(echo_config)
    get_and_put(Connection("10.100.100.2", config=config))
```

```
$ fab get-and-put2
10.100.100.2: test -e /tmp/hoge
10.100.100.2: cat /tmp/hoge
hoge
10.100.100.2: cat /tmp/hoge2
hoge
```

## タスクのヘルプ、引数について

- docstring を定義するとタスクのヘルプとして利用されます
- 引数を定義すると、自動的にタスクの実行引数として利用されます
  - デフォルト値を定義してない場合は入力必須の引数として扱われます

```
@task
def echo_arg(c, arg1, arg2, defaultarg="hoge"):
    "echo kwargs"
    c.run("echo arg1={}, arg2={}, defaultarg={}".format(arg1, arg2, defaultarg))
```

```
# 頭文字がそのまま省略引数として利用できます（頭文字がかぶってる場合はその次の文字が省略引数として設定されます）
$ fab -h echo-arg
Usage: fab [--core-opts] echo-arg [--options] [other tasks here ...]

Docstring:
  echo kwargs

Options:
  -a STRING, --arg1=STRING
  -d STRING, --defaultarg=STRING
  -r STRING, --arg2=STRING
```

```
$ fab echo-arg
'echo-arg' did not receive required positional arguments: 'arg1', 'arg2'

$ fab echo-arg --arg1 hoge --arg2 piyo
arg1=hoge, arg2=piyo, defaultarg=hoge

$ fab echo-arg --arg1 hoge --arg2 piyo --defaultarg=foo
arg1=hoge, arg2=piyo, defaultarg=foo
```

## テストについて

- pytest を使う

```
@task
def test_sample(c):
    return c.run("hostname")
```

```
from invoke import MockContext, Result
from fabfile import test_sample


def test_test_sample():
    c = MockContext(run={
        "hostname": Result("hoge.example.com"),
    })
    assert "hoge.example.com" in test_sample(c).stdout
```

```
$ pytest
```
