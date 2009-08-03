from abjad import *


def test_listtools_zip_cyclic_01( ):
   '''zip_cyclic can take two non-iterables.'''

   t = listtools.zip_cyclic(1, 2)
   assert t == [(1, 2)]


def test_listtools_zip_cyclic_02( ):
   '''zip_cyclic can take a list of length 1 and a non-iterables.'''

   t = listtools.zip_cyclic([1], 2)
   assert t == [(1, 2)]
   t = listtools.zip_cyclic(1, [2])
   assert t == [(1, 2)]


def test_listtools_zip_cyclic_03( ):
   '''zip_cyclic can take two lists of the same size.'''

   t = listtools.zip_cyclic([1, 2], ['a', 'b'])
   assert t == [(1, 'a'), (2, 'b')]


def test_listtools_zip_cyclic_04( ):
   '''zip_cyclic can take two lists of the different sizes.
      The list with the shortest size is cycled through.'''

   t = listtools.zip_cyclic([1, 2, 3], ['a', 'b'])
   assert t == [(1, 'a'), (2, 'b'), (3, 'a')]
   t = listtools.zip_cyclic([1, 2], ['a', 'b', 'c'])
   assert t == [(1, 'a'), (2, 'b'), (1, 'c')]


def test_listtools_zip_cyclic_05( ):
   '''Handle more than two iterables.'''

   a = [10, 11, 12]
   b = [20, 21]
   c = [30, 31, 32, 33]
   t = listtools.zip_cyclic(a, b, c)

   assert t == [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]
