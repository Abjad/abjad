from abjad.helpers.divisors import _divisors


def test_divisors_01( ):
   assert _divisors(1) == [1]
   assert _divisors(2) == [1, 2]
   assert _divisors(3) == [1, 3]
   assert _divisors(4) == [1, 2, 4]
   assert _divisors(5) == [1, 5]
   assert _divisors(6) == [1, 2, 3, 6]
   assert _divisors(7) == [1, 7]
   assert _divisors(8) == [1, 2, 4, 8]
   assert _divisors(9) == [1, 3, 9]
   assert _divisors(10) == [1, 2, 5, 10]
