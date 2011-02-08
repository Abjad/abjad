from fractions import Fraction
from abjad.tools import mathtools
from abjad.tools.mathtools.cumulative_sums_zero import cumulative_sums_zero
from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def pairwise_cumulative_sums_zero(sequence):
   '''Yield pairwise cumulative sums of `sequence` from ``0``::

      abjad> list(seqtools.iterate_sequence_pairwise_cumulative_sums_zero([1, 2, 3, 4, 5, 6]))
      [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

   Return pair generator.
   '''

   return iterate_sequence_pairwise_strict(cumulative_sums_zero(sequence))
