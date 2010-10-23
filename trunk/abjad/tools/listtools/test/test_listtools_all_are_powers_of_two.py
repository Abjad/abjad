from abjad import *


def test_listtools_all_are_powers_of_two_01( ):

   assert listtools.all_are_powers_of_two([ ])
   assert listtools.all_are_powers_of_two([1])
   assert listtools.all_are_powers_of_two([1, 2, 256, 8, 16, 16, 16])


def test_listtools_all_are_powers_of_two_02( ):

   assert not listtools.all_are_powers_of_two([3])
   assert not listtools.all_are_powers_of_two([1, 2, 4, 8, 16, 17])
