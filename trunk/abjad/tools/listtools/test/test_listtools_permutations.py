from abjad import *


def test_listtools_permutations_01( ):
   
   l = [1, 2, 3]
   t = listtools.permutations(l)
   t = list(t)

   assert t == [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
