from abjad import *
import py.test


def test_mathtools_divisors_01( ):
   assert mathtools.divisors(1) == [1]
   assert mathtools.divisors(2) == [1, 2]
   assert mathtools.divisors(3) == [1, 3]
   assert mathtools.divisors(4) == [1, 2, 4]
   assert mathtools.divisors(5) == [1, 5]
   assert mathtools.divisors(6) == [1, 2, 3, 6]
   assert mathtools.divisors(7) == [1, 7]
   assert mathtools.divisors(8) == [1, 2, 4, 8]
   assert mathtools.divisors(9) == [1, 3, 9]
   assert mathtools.divisors(10) == [1, 2, 5, 10]


def test_mathtools_divisors_02( ):
   assert py.test.raises(TypeError, 'mathtools.divisors(7.5)')
   assert py.test.raises(ValueError, 'mathtools.divisors(-1)')
