from abjad.helpers.pair_multiply_naive import _pair_multiply_naive
from abjad import *


def test_pair_multiply_naive_01( ):
   t = _pair_multiply_naive((4, 8), Rational(4, 5))
   assert t == (16, 40)


def test_pair_multiply_naive_02( ):
   t = _pair_multiply_naive((4, 8), Rational(3, 4))
   assert t == (12, 32)
