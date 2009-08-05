from abjad import *


def test_durtools_pair_multiply_naive_01( ):
   t = durtools.pair_multiply_naive((4, 8), Rational(4, 5))
   assert t == (16, 40)


def test_durtools_pair_multiply_naive_02( ):
   t = durtools.pair_multiply_naive((4, 8), Rational(3, 4))
   assert t == (12, 32)
