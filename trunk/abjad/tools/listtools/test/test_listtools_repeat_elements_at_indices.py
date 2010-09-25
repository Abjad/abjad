from abjad import *


def test_listtools_repeat_elements_at_indices_01( ):
   '''Excepted case.'''

   t = list(listtools.repeat_elements_at_indices(range(10), [6, 7, 8], 3))
   assert t == [0, 1, 2, 3, 4, 5, [6, 6, 6], [7, 7, 7], [8, 8, 8], 9]


def test_listtools_repeat_elements_at_indices_02( ):
   '''Boundary cases.'''

   t = list(listtools.repeat_elements_at_indices(range(10), [ ], 99))
   assert t == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

   t = list(listtools.repeat_elements_at_indices(range(10), range(10), 1))
   assert t == [[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]

   t = list(listtools.repeat_elements_at_indices(range(10), range(10), 2))
   assert t == [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], 
      [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

   t = list(listtools.repeat_elements_at_indices(range(10), [6, 7, 8], 0))
   assert t == [0, 1, 2, 3, 4, 5, [ ], [ ], [ ], 9]
