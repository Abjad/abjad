from abjad import *
from abjad.tools import durtools


def test_durtools_positive_integer_to_implied_prolation_multipler_01():
    '''Return the prolation that positive integer denominator carries.'''

    assert durtools.positive_integer_to_implied_prolation_multipler(1) == Fraction(1)
    assert durtools.positive_integer_to_implied_prolation_multipler(2) == Fraction(1)
    assert durtools.positive_integer_to_implied_prolation_multipler(3) == Fraction(2, 3)
    assert durtools.positive_integer_to_implied_prolation_multipler(4) == Fraction(1)
    assert durtools.positive_integer_to_implied_prolation_multipler(5) == Fraction(4, 5)
    assert durtools.positive_integer_to_implied_prolation_multipler(6) == Fraction(2, 3)
    assert durtools.positive_integer_to_implied_prolation_multipler(7) == Fraction(4, 7)
    assert durtools.positive_integer_to_implied_prolation_multipler(8) == Fraction(1)
    assert durtools.positive_integer_to_implied_prolation_multipler(9) == Fraction(8, 9)
    assert durtools.positive_integer_to_implied_prolation_multipler(10) == Fraction(4, 5)
    assert durtools.positive_integer_to_implied_prolation_multipler(11) == Fraction(8, 11)
    assert durtools.positive_integer_to_implied_prolation_multipler(12) == Fraction(2, 3)

