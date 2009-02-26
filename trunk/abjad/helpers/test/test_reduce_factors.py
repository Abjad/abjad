from abjad.helpers.reduce_factors import _reduce_factors
from abjad import *


def test_reduce_factors_01( ):
   assert _reduce_factors((4, 8), Rational(2, 3)) == (4, 12)


def test_reduce_factors_02( ):
   assert _reduce_factors((4, 8), Rational(4, 1)) == (4, 2)


def test_reduce_factors_03( ):
   assert _reduce_factors((4, 8), Rational(3, 5)) == (12, 40)


def test_reduce_factors_04( ):
   assert _reduce_factors((4, 8), Rational(6, 5)) == (12, 20)


def test_reduce_factors_05( ):
   assert _reduce_factors((5, 6), Rational(6, 5)) == (1, 1)
