from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_nonnegative_integer_01():

    assert mathtools.is_nonnegative_integer(1)
    assert mathtools.is_nonnegative_integer(long(1))
    assert mathtools.is_nonnegative_integer(Duration(1, 1))
    assert mathtools.is_nonnegative_integer(1.0)
    assert mathtools.is_nonnegative_integer(True)
    assert mathtools.is_nonnegative_integer(0)
    assert mathtools.is_nonnegative_integer(False)


def test_mathtools_is_nonnegative_integer_02():

    assert not mathtools.is_nonnegative_integer(-99)


def test_mathtools_is_nonnegative_integer_03():

    assert not mathtools.is_nonnegative_integer('foo')
