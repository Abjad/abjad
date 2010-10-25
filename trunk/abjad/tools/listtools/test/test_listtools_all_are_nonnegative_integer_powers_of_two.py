from abjad import *


def test_listtools_all_are_nonnegative_integer_powers_of_two_01( ):
   '''True when all elements in sequence are nonnegative integer powers of two.
   '''

   assert listtools.all_are_nonnegative_integer_powers_of_two([1, 2, 256, 8, 16, 16, 16])


def test_listtools_all_are_nonnegative_integer_powers_of_two_02( ):
   '''True on empty sequence.
   '''

   assert listtools.all_are_nonnegative_integer_powers_of_two([ ])


def test_listtools_all_are_nonnegative_integer_powers_of_two_03( ):
   '''False otherwise.
   '''

   assert not listtools.all_are_nonnegative_integer_powers_of_two([3])
   assert not listtools.all_are_nonnegative_integer_powers_of_two([1, 2, 4, 8, 16, 17])
