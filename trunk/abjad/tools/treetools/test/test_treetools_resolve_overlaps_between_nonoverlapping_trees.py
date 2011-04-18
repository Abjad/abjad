from abjad.tools.treetools import BoundedInterval
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools import resolve_overlaps_between_nonoverlapping_trees


def test_treetools_resolve_overlaps_between_nonoverlapping_trees_01( ):
   a = IntervalTree(BoundedInterval(0, 4, 'a'))
   b = IntervalTree(BoundedInterval(1, 5, 'b'))
   c = IntervalTree(BoundedInterval(2, 6, 'c'))
   d = IntervalTree(BoundedInterval(1, 3, 'd'))
   result = resolve_overlaps_between_nonoverlapping_trees([a, b, c, d])
   assert result == \
   IntervalTree([
      BoundedInterval(0, 4, 'a'),
      BoundedInterval(4, 5, 'b'),
      BoundedInterval(5, 6, 'c')
   ])
