from abjad import *


def test_listtools_arithmetic_mean_01( ):
   '''Return an exact integer or rational.'''
   
   assert listtools.arithmetic_mean([1, 2, 3, 4, 5]) == 3
   assert listtools.arithmetic_mean([10, 10, 10]) == 10
   assert listtools.arithmetic_mean([1, 1, 2, 3, 10]) == Rational(17, 5)
   assert listtools.arithmetic_mean([0, 1, 10]) == Rational(11, 3)


def test_listtools_arithmetic_mean_02( ):
   '''Return float.'''

   assert listtools.arithmetic_mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0
   assert listtools.arithmetic_mean([10, 10, 10.0]) == 10.0
