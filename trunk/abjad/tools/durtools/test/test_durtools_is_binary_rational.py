from abjad import *
from abjad.tools import durtools


def test_durtools_is_binary_rational_01( ):
    '''True when expr is int or fraction with denominator of the form 2**n.
    '''

    assert durtools.is_binary_rational(Fraction(1, 1))
    assert durtools.is_binary_rational(Fraction(1, 2))
    assert not durtools.is_binary_rational(Fraction(1, 3))
    assert durtools.is_binary_rational(Fraction(1, 4))
    assert not durtools.is_binary_rational(Fraction(1, 5))
    assert not durtools.is_binary_rational(Fraction(1, 6))
    assert not durtools.is_binary_rational(Fraction(1, 7))
    assert durtools.is_binary_rational(Fraction(1, 8))
    assert not durtools.is_binary_rational(Fraction(1, 9))
    assert not durtools.is_binary_rational(Fraction(1, 10))
    assert not durtools.is_binary_rational(Fraction(1, 11))
    assert not durtools.is_binary_rational(Fraction(1, 12))

    assert durtools.is_binary_rational(1)
    assert durtools.is_binary_rational(2)
    assert durtools.is_binary_rational(3)
    assert durtools.is_binary_rational(4)
    assert durtools.is_binary_rational(5)


def test_durtools_is_binary_rational_02( ):
    '''False when expr is nonint / nonfraction.
    '''

    assert not durtools.is_binary_rational(1.0)
    assert not durtools.is_binary_rational('foo')
