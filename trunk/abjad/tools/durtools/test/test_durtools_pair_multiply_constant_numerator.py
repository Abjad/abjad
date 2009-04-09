from abjad import *


def test_durtools_pair_multiply_constant_numerator_01( ):
   t = durtools.pair_multiply_constant_numerator((9, 16), Rational(2, 3))
   assert t == (9, 24)


def test_durtools_pair_multiply_constant_numerator_02( ):
   t = durtools.pair_multiply_constant_numerator((9, 16), Rational(1, 2))
   assert t == (9, 32)


def test_durtools_pair_multiply_constant_numerator_03( ):
   t = durtools.pair_multiply_constant_numerator((9, 16), Rational(5, 6))
   assert t == (45, 96)


def test_durtools_pair_multiply_constant_numerator_04( ):
   t = durtools.pair_multiply_constant_numerator((3, 8), Rational(2, 3))
   assert t == (3, 12)
