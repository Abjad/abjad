from abjad import *


def test_listtools_are_assignable_integers_01( ):
   '''True when the elements of l are all notehead assignable.'''

   l = [1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16]
   assert listtools.are_assignable_integers(l)

   l = [4, 4, 4, 4, 4, 4, 4]
   assert listtools.are_assignable_integers(l)

   l = [4]
   assert listtools.are_assignable_integers(l)


def test_listtools_are_assignable_integers_02( ):
   '''False when the elements of l are not all notehead assignable.'''

   l = [5, 9, 10, 11, 13]
   assert not listtools.are_assignable_integers(l)

   l = [4, 4, 4, 4, 5, 4, 4]
   assert not listtools.are_assignable_integers(l)

   l = [5]
   assert not listtools.are_assignable_integers(l)


def test_listtools_are_assignable_integers_03( ):
   '''True by definition when l is empty.'''

   l = [ ]
   assert listtools.are_assignable_integers(l)
