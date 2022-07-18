import getpass
from random import randint
from time import sleep
from concurrent.futures import ThreadPoolExecutor

from fabric import task, Connection, SerialGroup, ThreadingGroup, Config
from invoke import run

@task
def helloworld(c):
    print("c is {}".format(type(c)))
    run("hostname")
    c.local("hostname")
    c.run("hostname")


@task
def helloworld2(c):
    print("c is {}".format(type(c)))
    run("hostname")
    c.run("hostname")


@task
def hostname(c):
    result = Connection("10.100.100.2").run("hostname")
    result = _hostname(Connection("10.100.100.3"))


@task
def hostname_serial_group(c):
    result = SerialGroup("10.100.100.2", "10.100.100.3").run("hostname")
    print("---")
    result = _hostname(SerialGroup("10.100.100.3", "10.100.100.4"))


def _hostname(c):
    result = c.run("hostname")


@task
def hostname_threading_group(c):
    result = ThreadingGroup("10.100.100.2", "10.100.100.3").run("hostname")
    print("---")
    result = _hostname_sleep(ThreadingGroup("10.100.100.3", "10.100.100.4"))


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


@task
def sudo_hostname(c):
    c.sudo("hostname")


@task
def sudo_hostname_serial_group(c):
    result = SerialGroup("10.100.100.2", "10.100.100.3", config=c.config).sudo("hostname")


@task
def sudo_hostname2(c):
    sudo_pass = getpass.getpass("Input your sudo password > ")
    config = Config()
    config['sudo'] = {'password': sudo_pass}
    result = SerialGroup("10.100.100.2", "10.100.100.3", config=config).sudo("hostname")


@task
def touch_if_not_exists(c):
    print("start")
    c.run("test -e /tmp/hoge")
    print("end")


@task
def touch_if_not_exists2(c):
    print("start")
    if c.run("test -e /tmp/hoge", warn=True).failed:
        c.run("echo 'hoge' > /tmp/hoge")
    else:
        print("already exists")
    c.run("cat /tmp/hoge")
    print("end")


@task
def get_and_put(c):
    if c.run("test -e /tmp/hoge", warn=True).failed:
        c.run("echo 'hoge' > /tmp/hoge")

    c.get("/tmp/hoge", "/tmp/hoge")
    c.local("cat /tmp/hoge")

    c.put("/tmp/hoge", "/tmp/hoge2")
    c.run("cat /tmp/hoge2")


@task
def get_and_put2(c):
    config = Config()
    echo_config = {"echo": True, "echo_format": "10.100.100.2: {command}"}
    config["run"].update(echo_config)
    config["sudo"].update(echo_config)
    get_and_put(Connection("10.100.100.2", config=config))


@task
def echo_arg(c, arg1, arg2, defaultarg="hoge"):
    "echo kwargs"
    c.run("echo arg1={}, arg2={}, defaultarg={}".format(arg1, arg2, defaultarg))
