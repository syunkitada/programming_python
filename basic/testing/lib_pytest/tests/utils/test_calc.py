import unittest
from pkg.utils import calc


def test_add_num():
    assert 5 == calc.add_num(2, 3)
