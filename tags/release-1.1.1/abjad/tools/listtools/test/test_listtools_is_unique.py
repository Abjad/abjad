from abjad import *


def test_listtools_is_unique_01( ):
   '''True when the elements in input iterable are unique.'''

   assert listtools.is_unique([1, 2, 3])


def test_listtools_is_unique_02( ):
   '''False when the elements in input iterable are not unique.'''

   assert not listtools.is_unique([1, 1, 1, 2, 3])
