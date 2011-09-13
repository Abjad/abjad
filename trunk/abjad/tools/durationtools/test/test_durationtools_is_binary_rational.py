from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_binary_rational_01():
    '''True when expr is int or fraction with denominator of the form 2**n.
    '''

    assert durationtools.is_binary_rational(Fraction(1, 1))
    assert durationtools.is_binary_rational(Fraction(1, 2))
    assert not durationtools.is_binary_rational(Fraction(1, 3))
    assert durationtools.is_binary_rational(Fraction(1, 4))
    assert not durationtools.is_binary_rational(Fraction(1, 5))
    assert not durationtools.is_binary_rational(Fraction(1, 6))
    assert not durationtools.is_binary_rational(Fraction(1, 7))
    assert durationtools.is_binary_rational(Fraction(1, 8))
    assert not durationtools.is_binary_rational(Fraction(1, 9))
    assert not durationtools.is_binary_rational(Fraction(1, 10))
    assert not durationtools.is_binary_rational(Fraction(1, 11))
    assert not durationtools.is_binary_rational(Fraction(1, 12))

    assert durationtools.is_binary_rational(1)
    assert durationtools.is_binary_rational(2)
    assert durationtools.is_binary_rational(3)
    assert durationtools.is_binary_rational(4)
    assert durationtools.is_binary_rational(5)


def test_durationtools_is_binary_rational_02():
    '''False when expr is nonint / nonfraction.
    '''

    assert not durationtools.is_binary_rational(1.0)
    assert not durationtools.is_binary_rational('foo')
