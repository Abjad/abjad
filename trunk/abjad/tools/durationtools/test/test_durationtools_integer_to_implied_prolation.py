from abjad import *
from abjad.tools import durationtools


def test_durationtools_integer_to_implied_prolation_01():
    '''Return the prolation that positive integer denominator carries.'''

    assert durationtools.integer_to_implied_prolation(1) == Fraction(1)
    assert durationtools.integer_to_implied_prolation(2) == Fraction(1)
    assert durationtools.integer_to_implied_prolation(3) == Fraction(2, 3)
    assert durationtools.integer_to_implied_prolation(4) == Fraction(1)
    assert durationtools.integer_to_implied_prolation(5) == Fraction(4, 5)
    assert durationtools.integer_to_implied_prolation(6) == Fraction(2, 3)
    assert durationtools.integer_to_implied_prolation(7) == Fraction(4, 7)
    assert durationtools.integer_to_implied_prolation(8) == Fraction(1)
    assert durationtools.integer_to_implied_prolation(9) == Fraction(8, 9)
    assert durationtools.integer_to_implied_prolation(10) == Fraction(4, 5)
    assert durationtools.integer_to_implied_prolation(11) == Fraction(8, 11)
    assert durationtools.integer_to_implied_prolation(12) == Fraction(2, 3)
