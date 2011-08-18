from abjad import *


def test_tuplettools_is_proper_tuplet_multiplier_01():
    '''True when multiplier is a rational strictly greater than 1/2
        and strictly less than 2.'''

    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(1, 10))
    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(2, 10))
    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(3, 10))
    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(4, 10))
    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(5, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(6, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(7, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(8, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(9, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(10, 10))


def test_tuplettools_is_proper_tuplet_multiplier_02():
    '''True when multiplier is a rational strictly greater than 1/2
        and strictly less than 2.'''

    assert tuplettools.is_proper_tuplet_multiplier(Fraction(11, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(12, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(13, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(14, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(15, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(16, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(17, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(18, 10))
    assert tuplettools.is_proper_tuplet_multiplier(Fraction(19, 10))
    assert not tuplettools.is_proper_tuplet_multiplier(Fraction(20, 10))
