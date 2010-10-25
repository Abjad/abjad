from abjad import *


def test_listtools_all_are_equal_01( ):
   '''True when all elements in sequence are equal.
   '''

   assert listtools.all_are_equal([-1, -1, -1, -1, -1])
   assert listtools.all_are_equal([0, 0, 0, 0, 0])
   assert listtools.all_are_equal([1, 1, 1, 1, 1])
   assert listtools.all_are_equal([2, 2, 2, 2, 2])


def test_listtools_all_are_equal_02( ):
   '''True on empty sequence.
   '''

   assert listtools.all_are_equal([ ])


def test_listtools_all_are_equal_03( ):
   '''False otherwise.
   '''

   assert not listtools.all_are_equal([-1, -1, -1, -1, 99])
   assert not listtools.all_are_equal([0, 0, 0, 0, 99])
   assert not listtools.all_are_equal([1, 1, 1, 1, 99])
   assert not listtools.all_are_equal([2, 2, 2, 2, 99])
