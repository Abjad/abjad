from abjad.core import Fraction
from abjad.tools import mathtools
from abjad.tools.listtools.cumulative_sums_zero import cumulative_sums_zero
from abjad.tools.listtools.pairwise import pairwise


def pairwise_cumulative_sums_zero(l):
   '''Yield pairwise cumulative sums of ``l`` from ``0``::

      abjad> l = [1, 2, 3, 4, 5, 6]
      abjad> g = listtools.pairwise_cumulative_sums_zero(l)
      abjad> list(g)
      [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

   Note that this function returns a generator.
   '''

   return pairwise(cumulative_sums_zero(l))
