from abjad import *


def test_insert_slice_cyclic_01( ):
   '''Insert a copy of the elements of s between
      each of the elements of l.'''

   l = [0, 1, 2, 3, 4]
   s = ['A', 'B']

   t = listtools.insert_slice_cyclic(l, s)
   assert t == [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

   t = listtools.insert_slice_cyclic(l, s, overhang = (0, 1))
   assert t == [0, 'A', 'B', 1, 'A', 'B', 
                2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

   t = listtools.insert_slice_cyclic(l, s, overhang = (1, 0))
   assert t == ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 
             2, 'A', 'B', 3, 'A', 'B', 4]

   t = listtools.insert_slice_cyclic(l, s, overhang = (1, 1))
   assert t == ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 
             2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']
