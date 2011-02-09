from fractions import Fraction
from abjad.tools import mathtools
from abjad.tools.mathtools.cumulative_sums_zero import cumulative_sums_zero
from abjad.tools.seqtools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def list_pairwise_cumulative_sums_from_zero(sequence):
   '''List pairwise cumulative sums of `sequence` from ``0``::

      abjad> seqtools.iterate_sequence_pairwise_cumulative_sums_zero([1, 2, 3, 4, 5, 6])
      [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

   Return list of pairs.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.pairwise_cumulative_sums_zero( )`` to
      ``seqtools.list_pairwise_cumulative_sums_from_zero( )``.
   '''

   return list(iterate_sequence_pairwise_strict(cumulative_sums_zero(sequence)))
