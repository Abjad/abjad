from abjad.rational.rational import Rational
from abjad.tools import mathtools
from abjad.tools.listtools.pairwise import pairwise as listtools_pairwise


def pairwise_cumulative_sums(l):
   '''Yield pairwise cumulative sums of ``l`` from ``0``.

      ::

         abjad> l = [1, 2, 3, 4, 5, 6]
         abjad> g = listtools.pairwise_cumulative_sums(l)
         abjad> list(g)
         [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]'''

   assert isinstance(l, list)
   assert all([isinstance(x, (int, float, long, Rational)) for x in l])
   
   cumulative_sums = mathtools.sums(l) 
   cumulative_sums.insert(0, 0)
   return listtools_pairwise(cumulative_sums)
