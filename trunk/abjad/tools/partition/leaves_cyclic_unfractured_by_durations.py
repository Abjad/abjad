##from abjad.leaf.leaf import _Leaf
##from abjad.metricgrid.spanner import MetricGrid
##from abjad.tools import check
#from abjad.tools.partition.cyclic_unfractured_by_durations import \
#   cyclic_unfractured_by_durations as partition_cyclic_unfractured_by_durations
#
#
#def leaves_cyclic_unfractured_by_durations(leaves, durations):
#   '''Split leaves with split points taken cyclically from 'durations'.'''
#
#   return partition_cyclic_unfractured_by_durations(
#      leaves, durations, tie_after = True)
#
##   check.assert_components(
##      leaves, klasses = (_Leaf), contiguity = 'strict', share = 'thread')
##   mg = MetricGrid(leaves, durations)
##   mg.splitOnBar( )
##   mg.clear( )
