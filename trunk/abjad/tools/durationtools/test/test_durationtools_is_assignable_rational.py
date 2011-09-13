from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_assignable_rational_01():
    '''True expr is assignable rational. Otherwise false.
    '''

    assert not durationtools.is_assignable_rational(Fraction(0, 16))
    assert durationtools.is_assignable_rational(Fraction(1, 16))
    assert durationtools.is_assignable_rational(Fraction(2, 16))
    assert durationtools.is_assignable_rational(Fraction(3, 16))
    assert durationtools.is_assignable_rational(Fraction(4, 16))
    assert not durationtools.is_assignable_rational(Fraction(5, 16))


def test_durationtools_is_assignable_rational_02():
    '''False when expr is greater than value of 8 whole notes.
    '''

    assert durationtools.is_assignable_rational(1)
    assert durationtools.is_assignable_rational(2)
    assert durationtools.is_assignable_rational(4)
    assert durationtools.is_assignable_rational(8)
    assert not durationtools.is_assignable_rational(16)


def test_durationtools_is_assignable_rational_03():
    '''False when expr is nonrational type.
    '''

    assert not durationtools.is_assignable_rational(1.0)
    assert not durationtools.is_assignable_rational('foo')
