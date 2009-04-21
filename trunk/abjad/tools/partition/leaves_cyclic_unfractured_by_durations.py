from abjad.leaf.leaf import _Leaf
from abjad.metricgrid.spanner import MetricGrid
from abjad.tools import check


def leaves_cyclic_unfractured_by_durations(leaves, durations):
   '''Split leaves with split points taken cyclically from 'durations'.'''

   check.assert_components(
      leaves, klasses = (_Leaf), contiguity = 'strict', share = 'thread')
   mg = MetricGrid(leaves, durations)
   mg.splitOnBar( )
   mg.clear( )
