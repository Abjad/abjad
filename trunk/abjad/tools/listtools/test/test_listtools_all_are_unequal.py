from abjad import *


def test_listtools_all_are_unequal_01( ):
   '''True when the elements in input iterable are unique.'''

   assert listtools.all_are_unequal([1, 2, 3])


def test_listtools_all_are_unequal_02( ):
   '''False when the elements in input iterable are not unique.'''

   assert not listtools.all_are_unequal([1, 1, 1, 2, 3])
