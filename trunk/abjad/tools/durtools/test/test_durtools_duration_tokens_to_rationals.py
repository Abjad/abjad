from abjad import *
from abjad.tools import durtools


def test_durtools_duration_tokens_to_rationals_01( ):

   rationals = durtools.duration_tokens_to_rationals([Fraction(2, 4), 3, '8.', (5, 16)])

   assert rationals == [Fraction(1, 2), Fraction(3, 1), Fraction(3, 16), Fraction(5, 16)]
