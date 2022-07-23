from pkg.api import user
from pkg.db.user import UserDb


def test_get_user(mocker):
    # インスタンスのメソッドにpatchする
    user_db = UserDb()
    mocker.patch.object(user_db, "get", return_value={"name": "hoge", "age": 3})
    assert user.get_user(user_db, "hoge") == {"name": "hoge", "age": 3}


def test_get_user2(mocker):
    # インスタンスのメンバ変数にpatchする
    user_db = UserDb()
    mocker.patch.object(user_db, "database", {"piyo": {"name": "piyo", "age": 5}})
    assert user.get_user(user_db, "piyo") == {"name": "piyo", "age": 5}


def test_get_user3(mocker):
    # MagicMockを使う
    user_db = mocker.MagicMock()
    user_db.configure_mock(
        **{
            "get.return_value": {"name": "piyo", "age": 5},
        }
    )
    assert user.get_user(user_db, "piyo") == {"name": "piyo", "age": 5}


def test_get_user4(mocker):
    # MagicMockを使う(side_effect)
    user_db = mocker.MagicMock()
    user_db.configure_mock(
        **{
            "get.side_effect": lambda name: {"name": name, "age": 5},
        }
    )
    assert user.get_user(user_db, "piyo") == {"name": "piyo", "age": 5}
