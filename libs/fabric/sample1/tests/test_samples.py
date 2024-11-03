from invoke import MockContext, Result
from fabfile import thostname


def test_thostname():
    c = MockContext(run={
        "hostname": Result("hoge.example.com"),
    })
    assert "hoge.example.com" in thostname(c).stdout
