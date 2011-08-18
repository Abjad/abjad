from abjad import *
from abjad.tools import mathtools


def test_mathtools_is_assignable_integer_01():
    '''True when integer n can be written without
    recourse to ties. Otherwise false.
    '''

    assert not mathtools.is_assignable_integer(0)
    assert mathtools.is_assignable_integer(1)
    assert mathtools.is_assignable_integer(2)
    assert mathtools.is_assignable_integer(3)
    assert mathtools.is_assignable_integer(4)
    assert not mathtools.is_assignable_integer(5)
    assert mathtools.is_assignable_integer(6)
    assert mathtools.is_assignable_integer(7)
    assert mathtools.is_assignable_integer(8)


def test_mathtools_is_assignable_integer_02():

    assert not mathtools.is_assignable_integer(9)
    assert not mathtools.is_assignable_integer(10)
    assert not mathtools.is_assignable_integer(11)
    assert mathtools.is_assignable_integer(12)
    assert not mathtools.is_assignable_integer(13)
    assert mathtools.is_assignable_integer(14)
    assert mathtools.is_assignable_integer(15)
    assert mathtools.is_assignable_integer(16)
