from abjad import *


def test_durtools_multiply_duration_pair_01( ):
   t = durtools.multiply_duration_pair((4, 8), Rational(4, 5))
   assert t == (16, 40)


def test_durtools_multiply_duration_pair_02( ):
   t = durtools.multiply_duration_pair((4, 8), Rational(3, 4))
   assert t == (12, 32)
