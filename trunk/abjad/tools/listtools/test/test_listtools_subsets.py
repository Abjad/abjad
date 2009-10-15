from abjad import *


def test_listtools_subsets_01( ):

   l = [1, 2, 3, 4]
   generator = listtools.subsets(l)
   assert list(generator) == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]


def test_listtools_subsets_02( ):
   
   l = list('text')
   generator = listtools.subsets(l) 
   assert list(generator) == [[], ['t'], ['e'], ['t', 'e'], ['x'], ['t', 'x'], ['e', 'x'], ['t', 'e', 'x'], ['t'], ['t', 't'], ['e', 't'], ['t', 'e', 't'], ['x', 't'], ['t', 'x', 't'], ['e', 'x', 't'], ['t', 'e', 'x', 't']]
