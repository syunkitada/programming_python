from pkg.api import calc


def test_sum():
    assert calc.sum([1, 3, 6]) == 10


def test_sum_with_patch(mocker):
    # patchでモジュールの挙動を変えます(以下の計算結果は厳密には間違いである)
    mocker.patch("pkg.utils.calc.add_num", return_value=3)
    assert calc.sum([2, 1, 5]) == 3


def test_sum_with_patch2(mocker):
    # patchでモジュールの挙動を変えます(以下の計算結果は厳密には間違いである)
    def add_num(num1, num2):
        return num1 + num2 + 1

    mocker.patch("pkg.utils.calc.add_num", side_effect=add_num)
    assert calc.sum([2, 1, 5]) == 11


def test_sum_with_patch3(mocker):
    # patchでモジュールの挙動を変えます(以下の計算結果は厳密には間違いである)
    mocker.patch(
        "pkg.utils.calc.add_num", side_effect=lambda num1, num2: num1 + num2 + 2
    )
    assert calc.sum([2, 1, 5]) == 14


def test_sum_with_patch4(mocker):
    # patchでモジュールの挙動を変えます(例外を発生させる)
    mocker.patch("pkg.utils.calc.add_num", side_effect=Exception())
    assert calc.sum([2, 1, 5]) == -1
