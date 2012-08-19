from abjad import *
from abjad.tools import durationtools


def test_durationtools_positive_integer_to_implied_prolation_multiplier_01():
    '''Return the prolation that positive integer denominator carries.'''

    assert durationtools.positive_integer_to_implied_prolation_multiplier(1) == Fraction(1)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(2) == Fraction(1)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(3) == Fraction(2, 3)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(4) == Fraction(1)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(5) == Fraction(4, 5)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(6) == Fraction(2, 3)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(7) == Fraction(4, 7)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(8) == Fraction(1)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(9) == Fraction(8, 9)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(10) == Fraction(4, 5)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(11) == Fraction(8, 11)
    assert durationtools.positive_integer_to_implied_prolation_multiplier(12) == Fraction(2, 3)
