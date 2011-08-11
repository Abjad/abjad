from abjad import *
from abjad.tools import durtools


def test_durtools_is_assignable_rational_01( ):
    '''True expr is assignable rational. Otherwise false.
    '''

    assert not durtools.is_assignable_rational(Fraction(0, 16))
    assert durtools.is_assignable_rational(Fraction(1, 16))
    assert durtools.is_assignable_rational(Fraction(2, 16))
    assert durtools.is_assignable_rational(Fraction(3, 16))
    assert durtools.is_assignable_rational(Fraction(4, 16))
    assert not durtools.is_assignable_rational(Fraction(5, 16))


def test_durtools_is_assignable_rational_02( ):
    '''False when expr is greater than value of 8 whole notes.
    '''

    assert durtools.is_assignable_rational(1)
    assert durtools.is_assignable_rational(2)
    assert durtools.is_assignable_rational(4)
    assert durtools.is_assignable_rational(8)
    assert not durtools.is_assignable_rational(16)


def test_durtools_is_assignable_rational_03( ):
    '''False when expr is nonrational type.
    '''

    assert not durtools.is_assignable_rational(1.0)
    assert not durtools.is_assignable_rational('foo')

