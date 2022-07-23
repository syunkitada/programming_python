import pytest

from pkg.db import user


@pytest.fixture
def db():
    user_db = user.UserDb()
    user_db.insert("hoge", 11)
    user_db.insert("piyo", 18)
    return user_db


def test_get(db):
    assert db.get("hoge") == {"name": "hoge", "age": 11}
