from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_positive_integer_01():

    assert mathtools.is_positive_integer(1)
    assert mathtools.is_positive_integer(long(1))
    assert mathtools.is_positive_integer(Duration(1, 1))
    assert mathtools.is_positive_integer(1.0)
    assert mathtools.is_positive_integer(True)


def test_mathtools_is_positive_integer_02():

    assert not mathtools.is_positive_integer(-99)
    assert not mathtools.is_positive_integer(0)
    assert not mathtools.is_positive_integer(False)


def test_mathtools_is_positive_integer_03():

    assert not mathtools.is_positive_integer('foo')
