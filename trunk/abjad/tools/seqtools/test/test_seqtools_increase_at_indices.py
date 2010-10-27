from abjad import *


def test_seqtools_increase_at_indices_01( ):
   '''Increase elements of list l by the elements of addenda
      at indices in l.'''

   l = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
   t = seqtools.increase_at_indices(l, [0.5, 0.5], [0, 4, 8])
   assert t == [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]
