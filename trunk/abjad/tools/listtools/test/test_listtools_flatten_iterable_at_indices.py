from abjad import *



def test_listtools_flatten_iterable_at_indices_01( ):
   '''Works with positive indices.'''

   l = [0, 1, [2, 3, 4], [5, 6, 7]]
   t = listtools.flatten_iterable_at_indices(l, [2])

   assert t == [0, 1, 2, 3, 4, [5, 6, 7]]


def test_listtools_flatten_iterable_at_indices_02( ):
   '''Works with negative indices.'''

   l = [0, 1, [2, 3, 4], [5, 6, 7]]
   t = listtools.flatten_iterable_at_indices(l, [-1])

   assert t == [0, 1, [2, 3, 4], 5, 6, 7]


def test_listtools_flatten_iterable_at_indices_03( ):
   '''Boundary cases.'''

   l = [0, 1, [2, 3, 4], [5, 6, 7]]

   t = listtools.flatten_iterable_at_indices(l, [ ])
   assert t == [0, 1, [2, 3, 4], [5, 6, 7]]

   t = listtools.flatten_iterable_at_indices(l, [99])
   assert t == [0, 1, [2, 3, 4], [5, 6, 7]]

   t = listtools.flatten_iterable_at_indices(l, [-99])
   assert t == [0, 1, [2, 3, 4], [5, 6, 7]]
